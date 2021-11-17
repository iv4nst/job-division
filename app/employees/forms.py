from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import Employee, Job


class EditEmployeeForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2, max=30)])
    street = StringField('Street')
    street_number = StringField('Street number')
    city = StringField('City')
    country = StringField('Country')
    job = StringField('Job')
    submit = SubmitField('Update')
