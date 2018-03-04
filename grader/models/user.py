from grader import db
from flask_user import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Authentication information
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), unique=False, nullable=False)

    # User information
    first_name = db.Column(db.String(50), unique=False, nullable=False, server_default='')
    last_name = db.Column(db.String(50), unique=False, nullable=False, server_default='')
    email = db.Column(db.String(120), unique=True, nullable=False)
    active = db.Column('is_active', db.Boolean(), unique=False, nullable=False, server_default='0')
    confirmed_at = db.Column(db.DateTime())

    def __repr__(self):
        return '<User %r>' % self.username