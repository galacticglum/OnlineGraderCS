from flask_security.forms import RegisterForm, LoginForm
import wtforms
from wtforms import SelectField, TextField, SubmitField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField

class ExtendedRegisterForm(RegisterForm):
    first_name = TextField('First Name', [wtforms.validators.Required()])
    last_name = TextField('Last Name', [wtforms.validators.Required()])
    email = EmailField('Email Address', [wtforms.validators.Required(), wtforms.validators.Email()])

class ExtendedLoginForm(LoginForm):
    email = EmailField('Email Address', [wtforms.validators.Required(), wtforms.validators.Email()])

class SubmissionForm(FlaskForm):
    problem = SelectField('Problem', coerce=int, validators=[wtforms.validators.Required()])
    language = SelectField('Language', choices=[('0', 'Python'), ('1', 'C#'), ('2', 'Java')], validators=[wtforms.validators.Required()])
    file = FileField('File', [FileRequired()])
    submit = SubmitField('Submit')
