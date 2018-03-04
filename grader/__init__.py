from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_user import UserManager, SQLAlchemyAdapter

app = Flask(__name__, instance_relative_config = True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from grader.models.user import User

db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)
