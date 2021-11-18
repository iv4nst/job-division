from flask import render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user

from app import db
from app.employees import employees
from app.models import Employee, Job
from app.employees.forms import EditEmployeeForm


@employees.route('/employees_list', methods=['GET', 'POST'])
@login_required
def employees_list():
    all_employees = Employee.query.all()
    all_jobs = Job.query.all()

    return render_template('employees/employees_list.html', title='Employees', employees=all_employees, jobs=all_jobs)


@employees.route('/employee/add_to_job', methods=['GET', 'POST'])
@login_required
def add_to_job():
    # get selected employee and job
    unemployed = request.form.get('unemployed')  # chosen employee from list of unemployed
    job = request.form.get('job_id')  # chosen job from list of jobs

    # set job to that employee
    if unemployed and job:
        employee = Employee.query.get_or_404(unemployed)

        # employee.job_id = job
        employee.set_job(job)

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
    # TODO: Mozda staviti da bude request job change (i dugme za trazenje promene pored posla)
    #  stigne poruka adminu da je zatrazena promena, i onda se menja...

    if current_user.id != employee_id:
        abort(403)

    employee = Employee.query.get_or_404(employee_id)

    all_jobs = Job.query.all()
    form = EditEmployeeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            job = request.form.get('job_id')

            employee.first_name = form.first_name.data
            employee.last_name = form.last_name.data
            employee.street = form.street.data
            employee.street_number = form.street_number.data
            employee.city = form.city.data
            employee.country = form.country.data
            if job:
                employee.set_job(job)

            db.session.commit()
            return redirect(url_for('employees.profile', employee_id=employee_id))
        else:
            # if form.first_name.errors:
            #     error = 'Djole'
            error = [v[0] for k, v in form.errors.items()][0]
            return render_template('employees/profile-edit.html',
                                   employee=employee,
                                   jobs=all_jobs,
                                   form=form,
                                   message=error)
    return render_template('employees/profile-edit.html', employee=employee, jobs=all_jobs, form=form)

# TODO: Staviti dugme za brisanje posla (radnika sa posla), pored dropdown-a za posao u edit formi
