from flask import render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user

from app import db
from app.employees import employees
from app.models import Employee, Job


# from app.employees.forms import EditProfileForm


@employees.route('/employees_list', methods=['GET', 'POST'])
@login_required
def employees_list():
    all_employees = Employee.query.all()
    all_jobs = Job.query.all()

    # TODO: Staviti posao da na klik vodi na stranicu posla, kao profil kod radnika (napraviti stranicu)

    return render_template('employees/employees_list.html', title='Employees', employees=all_employees, jobs=all_jobs)


@employees.route('/employee/add_to_job', methods=['GET', 'POST'])
@login_required
def add_to_job():
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


@employees.route('/employee/<int:employee_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)

    if employee != current_user:
        db.session.delete(employee)
        db.session.commit()

    return redirect(url_for('employees.employees_list'))


@employees.route('/employee/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def profile(employee_id):
    """Employee profile"""
    employee = Employee.query.get_or_404(employee_id)

    return render_template('employees/profile.html', employee=employee)


@employees.route('/employee/<int:employee_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(employee_id):
    """Employee profile"""
    # TODO: Staviti da moze da se menja sifra i email (ako se menja email, mora sifra da se unese - mozda)
    # TODO: Staviti dugme edit profile ispod slike, u suprotnom message ili nesto tako
    if current_user.id != employee_id:
        abort(403)

    employee = Employee.query.get_or_404(employee_id)

    all_jobs = Job.query.all()

    # TODO: Mozda staviti da bude request job change (i dugme za trazenje promene pored posla)
    #  stigne poruka adminu da je zatrazena promena, i onda se menja...

    return render_template('employees/profile-edit.html', employee=employee, jobs=all_jobs)


@employees.route('/employee/<int:employee_id>/update', methods=['POST'])
@login_required
def update_profile(employee_id):
    """Employee profile"""
    if current_user.id != employee_id:
        abort(403)

    employee = Employee.query.get_or_404(employee_id)
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        street = request.form.get('street')
        street_number = request.form.get('street_number')
        city = request.form.get('city')
        country = request.form.get('country')
        job = request.form.get('job_title')

        # TODO: Srediti greske (isti email, broj...)

        employee.first_name = first_name
        employee.last_name = last_name
        employee.email = email
        employee.phone_number = phone_number
        employee.street = street
        employee.street_number = street_number
        employee.city = city
        employee.country = country
        if job:
            employee.job = job

        db.session.commit()
        return redirect(url_for('employees.profile', employee_id=employee_id))
    return render_template('employees/profile-edit.html', employee=employee)

# TODO: Staviti dugme za brisanje posla (radnika sa posla), pored dropdown-a za posao u edit formi
