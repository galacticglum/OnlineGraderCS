from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField
from wtforms.validators import DataRequired, Email

class AddContestForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    start_time = DateTimeField('start_time', validators=[DataRequired()])
    end_time = DateTimeField('end_time', validators=[DataRequired()])
