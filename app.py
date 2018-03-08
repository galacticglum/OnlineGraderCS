import os
import datetime

from flask import Flask, url_for, redirect, render_template, request, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from sqlalchemy.sql import func

# Create Flask application
app = Flask(__name__)
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

    def __str__(self):
        return self.name

class ContestParticipation(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.Integer, primary_key=True)
    join_time = db.Column(db.DateTime)

class Submission(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, primary_key=True)
    code = db.Column(db.String(1000))
    score = db.Column(db.Integer)

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
        # This is because our template checks whether the contest is null
        if contests.count() == 0:
            contests = None
        
    return render_template('index.html', contests=contests)

@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/contest/<int:contest_id>')
@login_required
def contest(contest_id):
    contest = db.session.query(Contest).filter(Contest.id == contest_id).first()

    # If the contest doesn't exist, we show a 404 error.
    if contest == None:
        abort(404)
        return

    participation_query = db.session.query(ContestParticipation).filter(ContestParticipation.user_id == current_user.id) \
        .filter(ContestParticipation.contest_id == contest_id)

    already_joined = participation_query.count() > 0

    if not already_joined:
        contest_participation = ContestParticipation(user_id=current_user.id, contest_id=contest_id, join_time=datetime.datetime.now())
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


def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import string
    import random

    db.drop_all()
    db.create_all()

    with app.app_context():
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()

        test_user = user_datastore.create_user(
            first_name='Admin',
            email='admin',
            password=encrypt_password('admin'),
            roles=[user_role, super_user_role]
        )

        first_names = [
            'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie', 'Sophie', 'Mia',
            'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
            'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
        ]
        last_names = [
            'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
            'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
            'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
        ]

        for i in range(len(first_names)):
            tmp_email = first_names[i].lower() + "." + last_names[i].lower() + "@example.com"
            tmp_pass = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))
            user_datastore.create_user(
                first_name=first_names[i],
                last_name=last_names[i],
                email=tmp_email,
                password=encrypt_password(tmp_pass),
                roles=[user_role, ]
            )
        db.session.commit()
    return

if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)
