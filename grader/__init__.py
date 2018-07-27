import __main__
import os

from flask import Flask, url_for
from instance.instance_config_setup import create_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from grader.forms import ExtendedLoginForm, ExtendedRegisterForm

from sqlalchemy.event import listens_for

# Create Flask application
application = Flask(__name__, instance_relative_config=True, instance_path=os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)), 'instance'))
application.config.from_object('default_settings')
application.config.from_pyfile('instance_base_config.py')
create_config(application)

db = SQLAlchemy(application)
migrate = Migrate(application, db)

# Setup Flask-Security
from grader.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(application, user_datastore, register_form=ExtendedRegisterForm, login_form=ExtendedLoginForm)

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

application.wsgi_app = ReverseProxied(application.wsgi_app)

# Get google credentials info
client_secret_path = os.path.join(application.instance_path, 'client_secret.json')
google_scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly']

# Create directory for file fields to use
upload_file_path = os.path.join(os.path.dirname(__file__), 'files')
try:
    os.mkdir(upload_file_path)
except OSError:
    pass

# This import will register all the routes, and it MUST be after we create the application
import grader.routes

# define a context processor for merging flask-admin's template context into the
# flask-security and app views.
import grader.utilities
@security.context_processor
@application.context_processor
def context_processor():
    return dict(
        get_url=url_for,
        formatted_datetime=grader.utilities.get_formatted_datetime,
        get_total_score=grader.utilities.get_total_score,
        get_user_full_name=grader.utilities.get_user_full_name,
        has_authenticated_with_google=grader.utilities.has_authenticated_with_google
    )