from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from app import db
from app.main import main
from app.models import Employee, Job


@main.route('/')
@login_required
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


@main.route('/employees_list', methods=['GET'])
@login_required
def employees_list():
    employees = Employee.query.all()
    jobs = Job.query.all()
    return render_template('employees_list.html', title='Employees', employees=employees, jobs=jobs)


@main.route('/jobs_list', methods=['GET', 'POST'])
@login_required
def jobs_list():
    jobs = Job.query.all()
    employees = Employee.query.all()

    # if jobs:
    return render_template('jobs_list.html', title='Jobs', jobs=jobs, employees=employees)


@main.route('/employees/<int:employee_id>', methods=['GET', 'POST'])
def profile(employee_id):
    """Employee profile"""
    employee = Employee.query.get_or_404(employee_id)

    return render_template('employee.html', employee=employee)
