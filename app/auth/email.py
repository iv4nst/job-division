from flask import render_template, current_app

from app.email import send_email


def send_password_reset_email(employee):
    token = employee.get_reset_password_token()

    send_email('[MicroBlog] Reset Your Password',
               sender=current_app.config['ADMIN_EMAIL'],
               recipients=[employee.email],
               text_body=render_template('email/reset_password.txt', employee=employee, token=token),
               html_body=render_template('email/reset_password.html', employee=employee, token=token))