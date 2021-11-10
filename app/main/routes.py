from flask import render_template
from flask_login import current_user, login_required

from app import db
from app.main import main
from app.models import Employee, Job


@main.before_app_request
def before_request():
    """
    Executes right before the view function.
    This code executes before any view function in the application.
    Check if user is logged in, and in that case do something.
    """
    if current_user.is_authenticated:
        db.session.commit()


@main.route('/')
# @login_required
def index():
    # all employees and jobs
    employees = Employee.query.all()
    jobs = Job.query.all()

    # number of employees and jobs
    num_of_employees = Employee.query.count()
    num_of_jobs = Job.query.count()

    return render_template('index.html',
                           employees=employees,
                           jobs=jobs,
                           num_of_employees=num_of_employees,
                           num_of_jobs=num_of_jobs)
