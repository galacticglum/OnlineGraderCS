from grader import db
from flask_security import UserMixin, RoleMixin

import datetime
import enum

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

problem_contests = db.Table(
    'problem_contests',
    db.Column('problem_id', db.Integer, db.ForeignKey('problem.id')),
    db.Column('contest_id', db.Integer, db.ForeignKey('contest.id'))
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

class ProblemDifficultyType(enum.Enum):
    easy = 0
    medium = 1
    hard  = 2

    def __str__(self):
        return self.name.capitalize()

    def to_html_str(self):
        if self == ProblemDifficultyType.easy:
            return 'success'
        elif self == ProblemDifficultyType.medium:
            return 'warning'
        elif self == ProblemDifficultyType.hard:
            return 'danger'

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    points = db.Column(db.Integer)
    difficulty = db.Column(db.Enum(ProblemDifficultyType))
    contests = db.relationship('Contest', secondary=problem_contests,
                                back_populates='problems')

    def __str__(self):
        return self.name

class Contest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    problems = db.relationship('Problem', secondary=problem_contests,
                                back_populates='contests')

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

class GoogleCredentials(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    credentials_json = db.Column(db.Text)
