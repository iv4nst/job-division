from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_email(subject, sender, recipients, text_body, html_body):
    with current_app.app_context():
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        Thread(target=mail.send(msg)).start()
