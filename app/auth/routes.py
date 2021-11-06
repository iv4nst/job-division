from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, current_user
import json

from app import db
from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import Employee
from app.auth.email import send_password_reset_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if request.method == 'POST':
        employee = Employee.query.filter_by(email=form.email.data).first()

        # login
        if form.validate():
            login_user(employee, remember=form.remember_me.data)
            return redirect(url_for('main.index'))
        # errors
        else:
            error = [v[0] for k, v in form.errors.items()][0]
            # error = form.email.errors[0] if form.email.errors else form.password.errors[0]
            return render_template('auth/login.html', title='Login', form=form, message=error)

    return render_template('auth/login.html', title='Login', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            employee = Employee(first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                email=form.email.data)
            employee.set_password(form.password.data)
            db.session.add(employee)
            db.session.commit()
            login_user(employee)
            return redirect(url_for('auth.login'))
        else:
            error = [v[0] for k, v in form.errors.items()][0]
            return render_template('auth/register.html', title='Register', form=form, message=error)

    return render_template('auth/register.html', title='Register', form=form)


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee:
            send_password_reset_email(employee)
            return render_template('email/email_sent.html', title='Email sent')
        else:
            error = 'Email not recognized.'
            return render_template('auth/reset_password_request.html', title='Forgot Password', form=form,
                                   message=error)

    return render_template('auth/reset_password_request.html', title='Forgot Password', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    # verify reset password token
    employee = Employee.verify_reset_password_token(token)
    if not employee:
        return redirect(url_for('main.index'))

    form = ResetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            employee.set_password(form.new_password.data)
            db.session.commit()
            return render_template('auth/password_reset_success.html')
        else:
            error = [v[0] for k, v in form.errors.items()][0]
            return render_template('auth/reset_password.html', form=form, message=error)

    return render_template('auth/reset_password.html', form=form)
