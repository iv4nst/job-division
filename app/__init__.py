from flask import Flask, request, current_app
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

from config import Config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login = LoginManager()
login.login_view = 'login'
login.login_message = 'Please log in to access this page.'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app, db)
    csrf = CSRFProtect(app)
    login = LoginManager(app)
    mail = Mail(app)


from app import routes, models
