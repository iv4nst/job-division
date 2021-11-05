from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app, msg)).start()


def send_password_reset_email(employee):
    token = employee.get_reset_password_token()

    send_email('[MicroBlog] Reset Your Password',
               sender=current_app.config['ADMIN_EMAIL'],
               recipients=[employee.email],
               text_body=render_template('email/reset_password.txt', employee=employee, token=token),
               html_body=render_template('email/reset_password.html', employee=employee, token=token))
