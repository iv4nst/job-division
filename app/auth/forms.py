from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import Employee, Job


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')

    def __init__(self, *k, **kk):
        self._user = None  # for internal user storing
        super(LoginForm, self).__init__(*k, **kk)

    def validate(self):
        self._user = Employee.query.filter(Employee.email == self.email.data).first()
        return super(LoginForm, self).validate()

    def validate_email(self, field):
        if self._user is None:
            raise ValidationError("Email not recognized.")

    def validate_password(self, field):
        if self._user is None:
            raise ValidationError()  # just to be sure
        if not self._user.check_password(self.password.data):  # password check embedded into employee model
            raise ValidationError("Incorrect password.")


class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=5,
                                                            message='Password must be at least 5 characters long.')])
    password_confirm = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        employee = Employee.query.filter_by(email=email.data).first()
        if employee:
            raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset')


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('Password',
                                 validators=[DataRequired(),
                                             Length(min=5, message='Password must be at least 5 characters long.')])
    new_password_confirm = PasswordField('Confirm Password',
                                         validators=[DataRequired(),
                                                     EqualTo('new_password', message='Passwords must match.')])
    submit = SubmitField('Reset Password')
