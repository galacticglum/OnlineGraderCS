import os
import datetime
import subprocess
import threading
import tempfile
import shutil
import uuid

import flask_admin
from flask import Flask, url_for, redirect, render_template, request, abort, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.event import listens_for
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from sqlalchemy.sql import func
from wtforms import Form, SelectField, FileField

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

    def __str__(self):
        return self.name

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    link = db.Column(db.String(255))
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
    score = db.Column(db.Integer)

class TestRun(db.Model):
    testcase_id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(application, user_datastore)

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
    form_overrides = {
        'link': flask_admin.form.FileUploadField
    }

    form_args = {
        'link' : {
            'label' : 'File',
            'base_path': upload_file_path,
            'allow_overwrite': False,
            'namegen': generate_problem_file_name
        }
    }

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

class SubmissionForm(Form):
    problem = SelectField('problem')
    language = SelectField('language')
    file = FileField('file')

def run_testcase_compiled(input_data, expected_output, testcase_id, submission_id, language_mode, exec_filepath, do_delete=False):
    if language_mode == 0: return

    command = str()
    if language_mode == 1:
        command = ["mono", exec_filepath]
    elif language_mode == 2:
        command = ["java", "-classpath", "{0}".format(exec_filepath), "Main"]

    output = subprocess.check_output(command, input=input_data, timeout=application.config['SCRIPT_RUN_TIMEOUT']).decode('utf-8')
    write_test_run(expected_output, output, testcase_id, submission_id)

    if do_delete:
        dir_path = exec_filepath
        if language_mode == 1:
            dir_path = os.path.dirname(os.path.realpath(exec_filepath))
        
        shutil.rmtree(dir_path)

def run_testcase_python(source_code, input_data, expected_output, testcase_id, submission_id, language_mode):
    if language_mode != 0: return

    output = subprocess.check_output(["python", "-c", source_code], input=input_data, timeout=application.config['SCRIPT_RUN_TIMEOUT']).decode('utf-8')
    write_test_run(expected_output, output, testcase_id, submission_id)

def write_test_run(expected_output, output, testcase_id, submission_id):
    with application.app_context():
        correct = Testcase.matches(expected_output, output.splitlines())
        test_run = TestRun(testcase_id=testcase_id, submission_id=submission_id, status=(1 if correct else -1))
        db.session.add(test_run)
        db.session.commit()

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

    return send_file(os.path.join(upload_file_path, problem.link))

@application.route('/contest/<int:contest_id>', methods=['GET', 'POST'])
@login_required
def contest(contest_id):
    form = SubmissionForm(request.form)
    contest = db.session.query(Contest).filter(Contest.id == contest_id).first()

    # If the contest doesn't exist, we show a 404 error.
    if contest == None:
        abort(404)
        return

    if request.method == 'POST':
        source_code = request.files['file'].read().decode('utf-8')

        submission = Submission(user_id=current_user.id, problem_id=form.problem.data, time=datetime.datetime.now(), code=source_code, score=0)
        db.session.add(submission)
        db.session.commit()

        problem = db.session.query(Problem).filter(Problem.id == form.problem.data).first()

        temp_dir = tempfile.mkdtemp()
        language_mode = int(form.language.data)
            
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

        return redirect(url_for('contest', contest_id=contest_id))
    else:
        # Check if the contest has expired or if it hasn't started yet
        if not contest.is_running():
            flash('Sorry, the contest you are trying to join is closed.', 'error')
            return redirect(url_for('index'))

        participation_query = db.session.query(ContestParticipation).filter(ContestParticipation.user_id == current_user.id) \
            .filter(ContestParticipation.contest_id == contest_id)

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
        return render_template('contest.html', contest=contest, time_left=time_left.total_seconds())

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
    )

if __name__ == '__main__':
    # Start app
    application.run(debug=True)
