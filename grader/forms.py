from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    first_name = StringField('firstname', validators=[DataRequired()])
    last_name = StringField('lastname', validators=[DataRequired()])
