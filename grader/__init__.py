from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_user import UserManager, SQLAlchemyAdapter

app = Flask(__name__, instance_relative_config = True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
#bcrypt = Bcrypt(app)

from grader.models.user import User
#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = 'login'

#@login_manager.user_loader
#def load_user(userid):
#    return User.query.filter(User.id == userid).first()

db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)
