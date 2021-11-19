from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired

from app.models import Employee


class EditProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2, max=30)])
    street = StringField('Street')
    street_number = StringField('Street number')
    city = StringField('City')
    country = StringField('Country')
    job = StringField('Job')
    submit = SubmitField('Update')


class EditAccountForm(FlaskForm):
    # TODO: Videti jel gotovo (da li treba ovi DataRequired()...)
    # TODO: Videti moze li da se koristi jedan submit (da proverava sta je od podataka uneto)

    # email change
    new_email = StringField('New Email', validators=[DataRequired(), Email()])
    submit1 = SubmitField('Change Email')

    # password change
    new_password = PasswordField('New Password', validators=[DataRequired(),
                                                             Length(min=5,
                                                                    message='Password must be at least 5 characters long.')])
    new_password_confirm = PasswordField('New Password Confirm', validators=[DataRequired(),
                                                                             EqualTo('new_password',
                                                                                     message='Passwords must match.')])
    submit2 = SubmitField('Change Password')

    current_password = PasswordField('Current Password', validators=[DataRequired()])

    def validate_new_email(self, email):
        employee = Employee.query.filter_by(email=email.data).first()
        if employee:
            raise ValidationError('Please use a different email.')
