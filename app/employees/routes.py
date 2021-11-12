from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app import db
from app.employees import employees
from app.models import Employee, Job


@employees.route('/employees_list', methods=['GET', 'POST'])
@login_required
def employees_list():
    all_employees = Employee.query.all()
    all_jobs = Job.query.all()

    return render_template('employees/employees_list.html', title='Employees', employees=all_employees, jobs=all_jobs)


@employees.route('/employee/new', methods=['GET', 'POST'])
@login_required
def add_employee():
    # TODO: Mozda izbrisati ovu opciju

    # get selected employee and job
    unemployed = request.form.get('unemployed')
    job = request.form.get('job_title')

    # set job to that employee
    if unemployed and job:
        employee = Employee.query.get_or_404(unemployed)

        employee.job = job

        db.session.add(employee)
        db.session.commit()

    return redirect(url_for('employees.employees_list'))


@employees.route('/employee/<int:employee_id>/update', methods=['POST', 'GET'])
@login_required
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        job = request.form.get('job_title')

        employee.first_name = first_name
        employee.last_name = last_name
        employee.email = email
        if phone_number:
            employee.phone_number = phone_number
        if job:
            employee.job = job
        db.session.commit()
        return redirect(url_for('employees.employees_list'))


@employees.route('/employee/<int:employee_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)

    if employee != current_user:
        db.session.delete(employee)
        db.session.commit()

    return redirect(url_for('employees.employees_list'))


@employees.route('/employees/<int:employee_id>', methods=['GET', 'POST'])
def profile(employee_id):
    """Employee profile"""
    employee = Employee.query.get_or_404(employee_id)

    return render_template('employees/employee.html', employee=employee)

# TODO: Staviti dugme za brisanje posla (radnika sa posla), pored dropdown-a za posao u edit formi
