import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Initialize flask
application = Flask(__name__, instance_relative_config=True,
    instance_path=os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'instance')))

application.config.from_pyfile('config_local.py')

jwt = JWTManager(application)
db = SQLAlchemy(application)

import grader.routes