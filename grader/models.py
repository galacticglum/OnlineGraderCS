from grader import db
from flask_security import UserMixin, RoleMixin
import datetime

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
    compiler_output = db.Column(db.Text)

    def get_language_name(self):
        if self.language == 0:
            return 'Python'
        
        if self.language == 1:
            return 'C#'

        if self.language == 2:
            return 'Java'

    def __str__(self):
        import grader.utilities
        return '#{0} at {1}'.format(self.id, grader.utilities.get_formatted_datetime(self.time))

class TestRun(db.Model):
    testcase_id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)
    output = db.Column(db.Text)

    def get_status_name(self):
        if self.status == 1:
            return "Correct"

        if self.status == 0:
            return "Pending"

        if self.status == -1 or self.status == -3:
            return "Failed"

        if self.status == -2:
            return "Timeout"

class GoogleCredentials(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    credentials_json = db.Column(db.Text)
