from flask import render_template, current_app

from app.email import send_email


def send_email_change_email(employee, new_email):
    token = employee.get_change_email_token()

    send_email('[Job-Division] Email Change Request',
               sender=current_app.config['ADMIN_EMAIL'],
               recipients=[new_email],
               text_body=render_template('email/change_email.txt', employee=employee, token=token, new_email=new_email),
               html_body=render_template('email/change_email.html', employee=employee, token=token,
                                         new_email=new_email))
