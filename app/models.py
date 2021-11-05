from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import json
import base64
import os

from app import db, login


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(140))
    employees = db.relationship('Employee', backref='working_as', lazy='dynamic')

    def __repr__(self):
        return f'<Job {self.title}>'


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    phone_number = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    job = db.Column(db.Integer, db.ForeignKey('job.title'))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'

    def set_password(self, password):
        """Set new password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if password is correct."""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """Check if user is admin."""
        admin_email = current_app.config['ADMIN_EMAIL']
        admin_pass = current_app.config['ADMIN_PASSWORD']
        return self.email == admin_email and self.check_password(admin_pass)

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


@login.user_loader
def load_user(employee_id):
    return Employee.query.get(int(employee_id))
