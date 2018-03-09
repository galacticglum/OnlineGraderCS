import datetime
import subprocess

from flask import Flask, url_for, redirect, render_template, request, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from sqlalchemy.sql import func
from wtforms import Form, SelectField, FileField

# Create Flask application
app = Flask(__name__, instance_relative_config = True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


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

    def matches(self, output):
        output_lines = self.output_data.splitlines()
        if len(output) != len(output_lines): return False
        for i in range(len(output)):
            if output_lines[i] != output[i]: return False

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
security = Security(app, user_datastore)

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

# Flask views
@app.route('/')
def index():
    contests = None
    if current_user.is_authenticated:
        contests = db.session.query(Contest)

        # We need to nullify our contests query if there are no elements.
        # This is because our template checks whether the contest is null (not the length)
        if contests.count() == 0:
            contests = None
        
    return render_template('index.html', contests=contests)

@app.route('/rules')
def rules():
    return render_template('rules.html')

class SubmissionForm(Form):
    problem = SelectField('problem')
    language = SelectField('language')
    file = FileField('file')

@app.route('/contest/<int:contest_id>', methods=['GET', 'POST'])
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
        submission_id = submission.id

        problem = db.session.query(Problem).filter(Problem.id == form.problem.data).first()
        for testcase in problem.testcases:
            binary_input = testcase.input_data.encode('utf-8')
            output = subprocess.check_output(["python", "-c", source_code], input=binary_input, timeout=app.config['SCRIPT_RUN_TIMEOUT']).decode('utf-8')

            correct = testcase.matches(output.splitlines())
            test_run = TestRun(testcase_id=testcase.id, submission_id=submission_id, status=(1 if correct else -1))
            db.session.add(test_run)
            db.session.commit()

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

            flash(f'Successfully joined {contest.name}!')
        else:
            contest_participation = participation_query.first()

        time_left = contest_participation.join_time + datetime.timedelta(minutes=contest.duration_minutes) - datetime.datetime.now()
        return render_template('contest.html', contest=contest, time_left=time_left.total_seconds())

# Create admin
admin = flask_admin.Admin(
    app,
    'Dashboard',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# Add model views
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Contest, db.session))
admin.add_view(MyModelView(Problem, db.session))
admin.add_view(MyModelView(Testcase, db.session))

# define a context processor for merging flask-admin's template context into the
# flask-security and app views.
@security.context_processor
@app.context_processor
def context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for,
    )

if __name__ == '__main__':
    # Start app
    app.run(debug=True)
