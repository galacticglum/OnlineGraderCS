from grader import application, db
from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    def __init__(self, username, no_hash_password, email):
        self.username = username
        self.password_hash = User.__generate_hash(no_hash_password)
        self.email = email

    @staticmethod
    def __generate_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def verify_hash(candidate_hash, actual_hash):
        return pwd_context.verify(candidate_hash, actual_hash)

    def to_json(self, include_password=False):
        json_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

        if include_password:
            json_dict['password'] = self.password_hash
        
        return json_dict

    @staticmethod
    def find_by_id(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def all():
        return {'users': [user.to_json() for user in UserModel.query.all()]}
    