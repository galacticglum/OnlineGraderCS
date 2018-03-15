import os
import io
import datetime
import subprocess
import threading
import tempfile
import shutil
import uuid

import flask_admin
import wtforms

from flask import Flask, url_for, redirect, render_template, request, abort, flash, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from flask_security.forms import RegisterForm, LoginForm
from flask_security.utils import encrypt_password
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from sqlalchemy.sql import func
from wtforms import Form, SelectField, StringField, TextField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.widgets import FileInput
from werkzeug.datastructures import FileStorage
from flask_wtf.file import FileRequired, FileField
from flask_wtf import FlaskForm
from sqlalchemy.event import listens_for

# Create Flask application
application = Flask(__name__, instance_relative_config = True)
application.config.from_object('config')
application.config.from_pyfile('config.py')
db = SQLAlchemy(application)

# Create directory for file fields to use
upload_file_path = os.path.join(os.path.dirname(__file__), 'files')
try:
    os.mkdir(upload_file_path)
except OSError:
    pass

# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

def get_formatted_datetime(datetime):
    return datetime.strftime('%b %d %Y, %I:%M %p')

def get_total_score(contest_id, user_id):
    contest = db.session.query(Contest).filter(Contest.id == contest_id).first()

    total_score = 0
    for problem in contest.problems:
        highest_scoring_submission = db.session.query(Submission).filter(Submission.user_id == user_id, \
        Submission.problem_id == problem.id).order_by(Submission.score.desc()).first()

        if highest_scoring_submission != None:
            total_score += highest_scoring_submission.score

    return total_score

def get_user_full_name(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    return (user.first_name if user.first_name else '') + (' ' + user.last_name if user.last_name else '')

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def has_role(self, role):
        return role in self.roles

    def __str__(self):
        return self.email

class Contest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)

    def has_started(self):
        return datetime.datetime.now() > self.start_time

    def has_expired(self):
        return datetime.datetime.now() > self.end_time

    def is_running(self):
        return self.has_started() and not self.has_expired()

    def has_duration_expired(self, contest_participation):
        return datetime.datetime.now() > contest_participation.join_time + datetime.timedelta(minutes=self.duration_minutes)

    def __str__(self):
        return self.name

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    pdf_link = db.Column(db.String(2083))
    total_points = db.Column(db.Integer)
    contest_id = db.Column(db.Integer, db.ForeignKey(Contest.id))
    contest = db.relationship('Contest', backref=db.backref('problems', lazy='dynamic'))

    def __str__(self):
        return self.name

class Testcase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    input_data = db.Column(db.Text)
    output_data = db.Column(db.Text)
    score_weight = db.Column(db.Integer)
    problem_id = db.Column(db.Integer, db.ForeignKey(Problem.id))
    problem = db.relationship('Problem', backref=db.backref('testcases', lazy='dynamic'))

    def matches(expected_output, real_output):
        if len(expected_output) != len(real_output): return False
        for i in range(len(expected_output)):
            if real_output[i] != expected_output[i]: return False

        return True

    def __str__(self):
        return self.name

class ContestParticipation(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.Integer, primary_key=True)
    join_time = db.Column(db.DateTime)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    problem_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    code = db.Column(db.Text)
    language = db.Column(db.Integer)
    score = db.Column(db.Integer)

    def get_language_name(self):
        if self.language == 0:
            return 'Python'
        
        if self.language == 1:
            return 'C#'

        if self.language == 2:
            return 'Java'

    def __str__(self):
        return '#{0} at {1}'.format(self.id, get_formatted_datetime(self.time))

class TestRun(db.Model):
    testcase_id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)

    def get_status_name(self):
        if self.status == 1:
            return "Correct"

        if self.status == 0:
            return "Pending"

        if self.status == -1:
            return "Failed"

        if self.status == -2:
            return "Timeout"

class ExtendedRegisterForm(RegisterForm):
    first_name = TextField('First Name', [wtforms.validators.Required()])
    last_name = TextField('Last Name', [wtforms.validators.Required()])
    email = EmailField('Email Address', [wtforms.validators.Required(), wtforms.validators.Email()])

class ExtendedLoginForm(LoginForm):
    email = EmailField('Email Address', [wtforms.validators.Required(), wtforms.validators.Email()])

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(application, user_datastore, register_form=ExtendedRegisterForm, login_form=ExtendedLoginForm)

# Create customized model view class
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

def generate_problem_file_name(object, file_data):
    return 'problem_{0}'.format(uuid.uuid4().hex)

class ProblemView(MyModelView):
    column_list = ('name','contest','total_points')
    form_overrides = {
        'pdf_link': flask_admin.form.FileUploadField
    }

    form_args = {
        'pdf_link' : {
            'label' : 'File',
            'base_path': upload_file_path,
            'allow_overwrite': False,
            'namegen': generate_problem_file_name,
            'validators':[wtforms.validators.Required()]
        }
    }

class SubmissionView(MyModelView):
    column_list = ('user_id', 'problem_id', 'time', 'language', 'score')
    form_widget_args = {
        'code' : {
            'readonly': True,
            'rows': 25
        }
    }

    column_formatters = dict(language=lambda v, c, m, p: m.get_language_name())

    can_create = False

# Delete hooks for models, delete files if models are getting deleted
@listens_for(Problem, 'after_delete')
def del_file(mapper, connection, target):
    if target.path:
        try:
            os.remove(op.join(upload_file_path, target.link))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass

# Flask views
@application.route('/')
def index():
    contests = None
    if current_user.is_authenticated:
        contests = db.session.query(Contest)

        # We need to nullify our contests query if there are no elements.
        # This is because our template checks whether the contest is null (not the length)
        if contests.count() == 0:
            contests = None
        
    return render_template('index.html', contests=contests)

@application.route('/rules')
def rules():
    return render_template('rules.html')

class SubmissionForm(FlaskForm):
    problem = SelectField('Problem', coerce=int, validators=[wtforms.validators.Required()])
    language = SelectField('Language', choices=[('0', 'Python'), ('1', 'C#'), ('2', 'Java')], validators=[wtforms.validators.Required()])
    file = FileField('File', [FileRequired()])
    submit = SubmitField('Submit')


def run_subprocess_safe(args, input_data):
    try:
        output = subprocess.check_output(args, input=input_data, timeout=application.config['SCRIPT_RUN_TIMEOUT']).decode('utf-8')
        return output, 0
    except subprocess.TimeoutExpired as _:
        return None, -2
    except:
        return None, -1
        

def run_testcase_compiled(input_data, expected_output, testcase_id, submission_id, language_mode, exec_filepath, do_delete=False):
    if language_mode == 0: return

    command = str()
    if language_mode == 1:
        command = ["mono", exec_filepath]
    elif language_mode == 2:
        command = ["java", "-classpath", "{0}".format(exec_filepath), "Main"]

    output, comp_status = run_subprocess_safe(command, input_data)
    write_test_run(expected_output, output, testcase_id, submission_id, comp_status)

    if do_delete:
        dir_path = exec_filepath
        if language_mode == 1:
            dir_path = os.path.dirname(os.path.realpath(exec_filepath))
        
        shutil.rmtree(dir_path)

def run_testcase_python(source_code, input_data, expected_output, testcase_id, submission_id, language_mode):
    if language_mode != 0: return

    output, comp_status = run_subprocess_safe(["python", "-c", source_code], input_data)
    write_test_run(expected_output, output, testcase_id, submission_id, comp_status)

def write_test_run(expected_output, output, testcase_id, submission_id, comp_status):
    with application.app_context():
        correct = False
        if output != None:
            correct = Testcase.matches(expected_output, output.splitlines())

        status = comp_status if comp_status != 0 else (1 if correct else -1)
        test_run = TestRun(testcase_id=testcase_id, submission_id=submission_id, status=status)
        db.session.add(test_run)

        submission = db.session.query(Submission).with_lockmode('update').filter(Submission.id == submission_id).first()
        problem = db.session.query(Problem).filter(Problem.id == submission.problem_id).first()
        testcase = db.session.query(Testcase).filter(Testcase.id == testcase_id).first()

        tries = 0

        # In case of a race condition or concurrent insert, we need to wait for the db to be unlocked.
        while tries < 50:
            try:
                submission.score = submission.score + (testcase.score_weight if correct else 0)
                db.session.commit()
                break
            except Exception as exec:
                db.session.rollback()

            tries += 1

@application.route('/problem/<int:problem_id>')
@login_required
def problem(problem_id):
    problem = db.session.query(Problem).filter(Problem.id == problem_id).first()
    if problem == None:
        abort(404)
        return

    participation_query = db.session.query(ContestParticipation).filter(ContestParticipation.user_id == current_user.id) \
        .filter(ContestParticipation.contest_id == problem.contest_id).first()

    if participation_query == None:
        abort(403)
        return

    return send_file(os.path.join(upload_file_path, problem.pdf_link), attachment_filename="problem{0}.pdf".format(problem.id), mimetype="application/pdf")

@application.route('/contest/<int:contest_id>', methods=['GET', 'POST'])
@login_required
def contest(contest_id):
    contest = db.session.query(Contest).filter(Contest.id == contest_id).first()

    # If the contest doesn't exist, we show a 404 error.
    if contest == None:
        abort(404)
        return
        
    form = SubmissionForm()
    form.problem.choices = [(problem.id, problem.name) for problem in contest.problems]

    participation_query = db.session.query(ContestParticipation).filter(ContestParticipation.user_id == current_user.id) \
        .filter(ContestParticipation.contest_id == contest_id)

    if form.validate_on_submit():
        if contest.has_duration_expired(participation_query.first()):
            flash('Sorry, unable to submit.', 'error')
            return redirect(url_for('contest', contest_id=contest_id))

        source_code = request.files['file'].read().decode('utf-8-sig')
        language_mode = int(form.language.data)
        submission = Submission(user_id=current_user.id, problem_id=form.problem.data, time=datetime.datetime.now(), code=source_code, score=0, language=language_mode)
        db.session.add(submission)
        db.session.commit()

        problem = db.session.query(Problem).filter(Problem.id == form.problem.data).first()

        temp_dir = tempfile.mkdtemp()
        temp_exec_file = None

        if language_mode != 0:
            temp_source_file = None
            temp_exec_file = None
            suffix = str()

            if language_mode == 2:
                suffix = ".java"
            else:
                temp_exec_file = tempfile.NamedTemporaryFile(dir=temp_dir, delete=False)
                temp_exec_file.close()

            temp_source_file = tempfile.NamedTemporaryFile(dir=temp_dir, mode='w', delete=False, suffix=suffix)
            temp_source_file.write(source_code)
            temp_source_file.close()

            if language_mode == 1:
                subprocess.call(["csc", "-out:{0}".format(temp_exec_file.name), temp_source_file.name])
            elif language_mode == 2:
                subprocess.call(["javac", temp_source_file.name])

            os.remove(temp_source_file.name)

        testcases = problem.testcases.all()
        for i in range(len(testcases)):
            testcase = testcases[i]

            binary_input = testcase.input_data.encode('utf-8')
            expected_output = testcase.output_data.splitlines()

            compile_thread = None
            if language_mode == 0:
                compile_thread = threading.Thread(target=run_testcase_python, args=(source_code, binary_input, expected_output, testcase.id, \
                    submission.id, language_mode))
            else:
                do_delete = i == len(testcases) - 1

                compile_thread = threading.Thread(target=run_testcase_compiled, args=(binary_input, expected_output, testcase.id, submission.id, \
                    language_mode, (temp_exec_file.name if language_mode == 1 else temp_dir), do_delete))
            
            compile_thread.start()

        return redirect(url_for('submission', submission_id=submission.id))
    else:
        # Check if the contest has expired or if it hasn't started yet
        if not contest.is_running():
            flash('Sorry, the contest you are trying to join is closed.', 'error')
            return redirect(url_for('index'))

        already_joined = participation_query.count() > 0

        if not already_joined:
            contest_participation = ContestParticipation(user_id=current_user.id, contest_id=contest_id, 
                join_time=datetime.datetime.now())
                
            db.session.add(contest_participation)
            db.session.commit()

            flash('Successfully joined {0}!'.format(contest.name))
        else:
            contest_participation = participation_query.first()

        time_left = contest_participation.join_time + datetime.timedelta(minutes=contest.duration_minutes) - datetime.datetime.now()

        submissions = []
        most_recent_submissions = {}
        highest_scoring_submissions = {}

        for problem in contest.problems:
            most_recent_submissions[problem] = db.session.query(Submission).filter(Submission.user_id == current_user.id, \
                Submission.problem_id == problem.id).order_by(Submission.time.desc()).first()

            highest_scoring_submissions[problem] = db.session.query(Submission).filter(Submission.user_id == current_user.id, \
                Submission.problem_id == problem.id).order_by(Submission.score.desc()).first()

            for submission in db.session.query(Submission).filter(Submission.user_id == current_user.id, Submission.problem_id == problem.id) \
                .order_by(Submission.time.desc()).all():
                submissions.append((problem, submission))

        can_submit = not contest.has_duration_expired(participation_query.first())
        return render_template('contest.html', contest=contest, submissions=submissions, time_left=time_left.total_seconds(), 
            submission_form=form, can_submit=can_submit, most_recent_submissions=most_recent_submissions, 
            highest_scoring_submissions=highest_scoring_submissions)

def get_scoreboard_results(contest_id):
    participations = db.session.query(User, ContestParticipation).filter(ContestParticipation.contest_id == contest_id) \
        .filter(User.id == ContestParticipation.user_id).all()

    scores = []
    for participation in participations:
        total_score = get_total_score(contest_id, participation[0].id)
        result_object = {}
        result_object['user'] = get_user_full_name(participation[0].id)
        result_object['total_score'] = total_score
        scores.append(result_object)

    return sorted(scores, reverse=True, key=lambda x: x['total_score'])

@application.route('/scoreboard/<int:contest_id>')
@login_required
def scoreboard(contest_id):
    if not current_user.has_role('superuser'):
        abort(403)
        return

    contest = db.session.query(Contest).filter(Contest.id == contest_id).first()

    # If the contest doesn't exist, we show a 404 error.
    if contest == None:
        abort(404)
        return

    return render_template('scoreboard.html', contest=contest, scores=get_scoreboard_results(contest_id))

@application.route('/scoreboard/results/<int:contest_id>')
@login_required
def scoreboard_results(contest_id):
    if not current_user.has_role('superuser'):
        abort(403)
        return

    contest = db.session.query(Contest).filter(Contest.id == contest_id).first()

    # If the contest doesn't exist, we show a 404 error.
    if contest == None:
        abort(404)
        return

    is_contest_closed = contest.has_expired()
    return jsonify(scores=get_scoreboard_results(contest_id), closed=is_contest_closed)

@application.route('/submission/<int:submission_id>')
@login_required
def submission(submission_id):
    submission = db.session.query(Submission).filter(Submission.id == submission_id).first()
    if submission == None:
        abort(404)
        return

    if submission.user_id != current_user.id:
        abort(403)
        return
 
    problem = db.session.query(Problem).filter(Problem.id == submission.problem_id).first()
    contest = db.session.query(Contest).filter(Contest.id == problem.contest_id).first()

    tests = []
    for testcase in problem.testcases:
        test_run = db.session.query(TestRun).filter(TestRun.testcase_id == testcase.id, TestRun.submission_id == submission_id).first()
        tests.append((testcase, test_run))

    return render_template('submission.html', submission=submission, contest=contest, problem=problem, tests=tests)

@application.route('/submission/results/<int:submission_id>')
@login_required
def submission_results(submission_id):
    submission = db.session.query(Submission).filter(Submission.id == submission_id).first()
    if submission == None:
        abort(404)
        return

    if submission.user_id != current_user.id:
        abort(403)
        return
 
    problem = db.session.query(Problem).filter(Problem.id == submission.problem_id).first()
    contest = db.session.query(Contest).filter(Contest.id == problem.contest_id).first()

    tests = []
    for testcase in problem.testcases:
        test_run = db.session.query(TestRun).filter(TestRun.testcase_id == testcase.id, TestRun.submission_id == submission_id).first()
        result_object = {}
        result_object['id'] = testcase.id
        result_object['status'] = test_run.status if test_run != None else 0
        result_object['status_name'] = 'None' if test_run == None else test_run.get_status_name()
        tests.append(result_object)

    return jsonify(tests)

# Create admin
admin = flask_admin.Admin(
    application,
    'Dashboard',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# Add model views
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Contest, db.session))
admin.add_view(ProblemView(Problem, db.session))
admin.add_view(MyModelView(Testcase, db.session))
admin.add_view(SubmissionView(Submission, db.session))

# define a context processor for merging flask-admin's template context into the
# flask-security and app views.
@security.context_processor
@application.context_processor
def context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for,
        formatted_datetime=get_formatted_datetime,
        get_total_score=get_total_score,
        get_user_full_name=get_user_full_name
    )

if __name__ == '__main__':
    # Start app
    application.run(debug=True)
