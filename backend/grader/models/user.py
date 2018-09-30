from grader import application, db
from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    """
    An object which holds information about a user.
    This model is used by Flask-SQLAlchemy to generate
    the "user" SQL database table.

    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    def __init__(self, username, plaintext_password, email):
        """
        Initializes a `User` object from a `username`, `plaintext_password`, and `email`.
        The provided `plaintext_password` is hashed using the sha256 cryptographic hash 
        function before it is saved in the model (in the variable `password_hash`).
        Hashing the password ensures that the password is secure because the original
        plaintext password cannot be retrieved from the hash.

        :param username:
            The username of the user.
        :param plaintext_password:
            The password of the user in plaintext. This value is never stored.
            It is hashed using the sha256 cryptographic hash function and then saved.
        :param email:
            The email address of the user.
        :returns:
            The new User object.
        """

        self.username = username
        self.password_hash = User.__generate_hash(plaintext_password)
        self.email = email

    @staticmethod
    def __generate_hash(password):
        """
        Generates a hashed value of the specified `password` value.

        :param password:
            the plaintext password to generate a hash of.
        :returns:
            the hash of the plaintext password.
        """

        return pwd_context.hash(password)

    @staticmethod
    def verify_hash(candidate_password, actual_hash):
        """
        Verifies a plaintext `candidate_password` with an `actual_hash`. 
        This is used for password verification where the `candidate_password`
        is a plaintext password that might potentially be the correct password.

        :param candidate_password:
            the plaintext password that might potentially be the correct password.
        :param actual_hash:
            the hash of the correct password (User.password_hash).
        :returns:
            a boolean indicating whether the candidate_password is the
            same as the password represented by the actual_hash.
            
            True if correct, False otherwise.
        """

        return pwd_context.verify(candidate_password, actual_hash)

    def to_json(self, include_password=False):
        """
        Converts this user to a dictionary object containing all user information.
        
        ``NOTE``: This should not be used to send user information to unauthenticated sources
        because it includes sensitive information such as email address.

        :param include_password:
            Indicates whether to include the hashed password of the user
            in the dictionary object (default=False).
        :returns:
            A dictionary that can be converted/serialized to JSON
        """

        json_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

        if include_password:
            json_dict['password'] = self.password_hash
        
        return json_dict

    def to_api_safe_json(self):
        """
        Converts this user to a dictionary object containing user information 
        that is safe to send to unauthenticated sources.

        :returns:
            A dictionary that can be converted/serialized to JSON
        """

        return {
            'id': self.id,
            'username': self.username
        }

    @staticmethod
    def find_by_id(id):
        """
        Finds a `User` object by it's id in the database.

        :param id:
            the id of the User to find.  
        :returns:
            The User object with the specified id or None
            if the user couldn't be found.
        """

        return User.query.filter_by(id=id).first()

    @staticmethod
    def find_by_username(username):
        """
        Finds a `User` object by it's username.

        :param username:
            the username of the User to find.  
        :returns:
            The User object with the specified username or None
            if the user couldn't be found.
        """

        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_by_email(email):
        """
        Finds a `User` object by it's email.

        :param email:
            the email of the User to find.  
        :returns:
            The User object with the specified email or None
            if the user couldn't be found.
        """

        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_by_username_and_email(username, email):
        """
        Finds a `User` object with the specified
        username and email.

        :param username:
            the username of the User to find.  
        :param email:
            the email of the User to find.
        :returns:
            The User object with the specified username and email or None
            if the user couldn't be found.
        """

        return User.query.filter_by(username=username, email=email).first()

    @staticmethod
    def all(json_converter_func=lambda x: x.to_api_safe_json()):
        """
        Gets a dictionary object containing all the users in the database.

        :param json_converter_func:
            a function that takes in a User object and converts it to a
            a dictionary object (default=User.to_api_safe_json).
        :returns:
            A dictionary object containing all the users in the database that can
            be converted/serialized as JSON.
        """

        
        return {'users': [json_converter_func(user) for user in User.query.all()]}
    