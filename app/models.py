from time import time
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from app import db, login


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    date_added = db.Column(db.DateTime, index=True, default=datetime.now)  # '%d %b, %Y'
    employees = db.relationship('Employee', backref='job', lazy='dynamic')

    def __repr__(self):
        return f'<Job {self.title}>'


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    street = db.Column(db.String(120), index=True)
    street_number = db.Column(db.String(32), index=True)
    city = db.Column(db.String(120), index=True)
    country = db.Column(db.String(64), index=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    # TODO: Napraviti posebno za admina

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'

    def set_password(self, password):
        """Set new password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if password is correct."""
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        """Get token for password reset."""
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        """
        Decode the password reset token.
        :param token: reset password token
        :return: employee id if token is valid
        """
        try:
            employee_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return Employee.query.get(employee_id)

    def get_change_email_token(self, expires_in=600):
        """Get token for email change."""
        return jwt.encode(
            {'change_email': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_change_email_token(token):
        """
        Decode the email change token.
        :param token: email change token
        :return: employee id if token is valid
        """
        try:
            employee_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['change_email']
        except:
            return
        return Employee.query.get(employee_id)

    def has_address(self):
        """True if employee has a valid address."""
        return self.street and self.street_number and self.city and self.country

    def set_job(self, job_id: int):
        self.job_id = job_id

    @property
    def get_street(self):
        return self.street or ''

    @property
    def get_street_number(self):
        return self.street_number or ''

    @property
    def get_city(self):
        return self.city or ''

    @property
    def get_country(self):
        return self.country or ''

    @property
    def address(self):
        """Get full address."""
        street = self.street if self.street else ''
        street_number = self.street_number if self.street_number else ''
        city = self.city if self.city else ''
        country = self.country if self.country else ''
        return f'{street} {street_number}, {city}, {country}'


@login.user_loader
def load_user(employee_id):
    return Employee.query.get(int(employee_id))
