from flask import render_template, redirect, url_for, request, abort, flash
from flask_login import login_required, current_user

from app import db
from app.employees.email import send_email_change_email
from app.employees import employees
from app.models import Employee, Job
from app.employees.forms import EditProfileForm, EditAccountForm


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


# ==================================================================================


@employees.route('/employee/<int:employee_id>/profile', methods=['GET', 'POST'])
@login_required
def profile(employee_id):
    """Employee profile"""
    employee = Employee.query.get_or_404(employee_id)

    return render_template('employees/profile.html', employee=employee)


@employees.route('/employee/<int:employee_id>/profile/edit', methods=['GET', 'POST'])
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
    form = EditProfileForm()
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


@employees.route('/employee/<int:employee_id>/account', methods=['GET', 'POST'])
@login_required
def edit_account(employee_id):
    """Employee account"""
    if current_user.id != employee_id:
        abort(403)

    employee = Employee.query.get_or_404(employee_id)

    form = EditAccountForm()

    # check if there is data to change
    new_email = form.new_email.data
    current_password = form.current_password.data
    new_password = form.new_password.data
    new_password_confirm = form.new_password_confirm.data

    if request.method == 'POST':
        # TODO: srediti kao za sifru dole, da ispisuje greske (ako treba da se sredi)
        # change email
        if request.form.get('change_email'):
            email_already_exists = Employee.query.filter_by(email=new_email).first()
            # send email
            if new_email and not email_already_exists:
                send_email_change_email(employee, new_email)
                return render_template('email/change_email_sent.html', title='Email sent', employee=employee)
            # already exists error
            elif email_already_exists:
                error = 'Please choose a different email.'
            # not provided error
            else:
                error = 'Please enter an email.'
            return render_template('employees/edit_account.html', employee=employee, form=form, email_error=error)

        # change password
        elif request.form.get('change_password'):
            if not current_password or not new_password or not new_password_confirm:
                error = 'All fields are required.'
            else:
                if not employee.check_password(current_password):
                    error = 'Incorrect password.'
                elif employee.check_password(current_password) == employee.check_password(new_password):
                    error = 'You cannot use your old password.'
                elif new_password != new_password_confirm:
                    error = 'Passwords must match.'
                elif len(new_password) < 5:
                    error = 'Password must be at least 5 characters long.'
                else:
                    # Change password
                    employee.set_password(new_password)
                    db.session.commit()
                    message = 'Your password has been changed.'
                    return render_template('employees/edit_account.html', employee=employee, form=form,
                                           message=message)
            return render_template('employees/edit_account.html', employee=employee, form=form,
                                   password_error=error)

    return render_template('employees/edit_account.html', employee=employee, form=form)


@employees.route('/change_email/<token>/<new_email>', methods=['GET', 'POST'])
def change_email(token, new_email):
    # verify reset email token
    employee = Employee.verify_change_email_token(token)
    if not employee:
        return redirect(url_for('main.index'))

    employee.email = new_email
    db.session.commit()

    return redirect(url_for('employees.profile', employee_id=employee.id))
