from grader import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True) # Change to not nullable when email is added
    _password = db.Column(db.String(128), unique=False, nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)

    def __repr__(self):
        return '<User %r>' % self.username