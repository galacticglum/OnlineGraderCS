import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth, MultiAuth

# Initialize flask
application = Flask(__name__, instance_relative_config=True,
    instance_path=os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'instance')))

application.config.from_pyfile('config_local.py')

token_auth = HTTPTokenAuth(scheme='Token')
basic_auth = HTTPBasicAuth()
auth = MultiAuth(basic_auth, token_auth)
db = SQLAlchemy(application)

import grader.routes