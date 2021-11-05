from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app import db
from app.employees import employees
from app.models import Employee


@employees.route('/employee/new', methods=['GET', 'POST'])
@login_required
def add_employee():
    # TODO: Namestiti da se unese i sifra kad se dodaje korisnik

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    job = request.form.get('job_title')

    already_exists = Employee.query.filter_by(email=email).first()
    # TODO: Staviti neku poruku ako postoji radnik
    # staviti ono validate u modelu
    # TODO: Srediti da ne mogu dva ista korisnika (isti mejl...i broj telefona)
    if not already_exists:
        employee = Employee(first_name=first_name,
                            last_name=last_name,
                            email=email)
        if job and job != 'Jobs':
            employee.job = job
        if phone_number:
            employee.phone_number = phone_number

        db.session.add(employee)
        db.session.commit()
    return redirect(url_for('employees_list'))


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
        return redirect(url_for('employees_list'))


@employees.route('/employee/<int:employee_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)

    if employee != current_user:
        db.session.delete(employee)
        db.session.commit()

    return redirect(url_for('employees_list'))
