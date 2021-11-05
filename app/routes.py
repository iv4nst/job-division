from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.models import Employee, Job
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email


@app.route('/')
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if request.method == 'POST':
        employee = Employee.query.filter_by(email=form.email.data).first()

        # login
        if form.validate():
            login_user(employee, remember=form.remember_me.data)
            return redirect(url_for('index'))
        # errors
        else:
            error = [v[0] for k, v in form.errors.items()][0]
            # error = form.email.errors[0] if form.email.errors else form.password.errors[0]
            return render_template('login.html', title='Login', form=form, error=error)

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            employee = Employee(first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                email=form.email.data)
            employee.set_password(form.password.data)
            db.session.add(employee)
            db.session.commit()
            login_user(employee)
            return redirect(url_for('login'))
        else:
            error = [v[0] for k, v in form.errors.items()][0]
            return render_template('register.html', title='Register', form=form, error=error)

    # if form.validate_on_submit():
    #     employee = Employee(first_name=form.first_name.data,
    #                         last_name=form.last_name.data,
    #                         email=form.email.data)
    #     employee.set_password(form.password.data)
    #     db.session.add(employee)
    #     db.session.commit()
    #     login_user(employee)
    #     return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['POST', 'GET'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee:
            send_password_reset_email(employee)
            return render_template('email_sent.html', title='Email sent')
        else:
            error = 'Email not recognized.'
            return render_template('reset_password_request.html', title='Forgot Password', form=form, error=error)

    return render_template('reset_password_request.html', title='Forgot Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    employee = Employee.verify_reset_password_token(token)
    if not employee:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        employee.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


# ================================================================================


@app.route('/employees_list', methods=['GET'])
@login_required
def employees_list():
    employees = Employee.query.all()
    jobs = Job.query.all()
    return render_template('employees_list.html', title='Employees', employees=employees, jobs=jobs)


@app.route('/employee/new', methods=['GET', 'POST'])
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


@app.route('/employee/<int:employee_id>/update', methods=['POST', 'GET'])
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


@app.route('/employee/<int:employee_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)

    if employee != current_user:
        db.session.delete(employee)
        db.session.commit()

    return redirect(url_for('employees_list'))


# ================================================================================


@app.route('/jobs_list', methods=['GET', 'POST'])
@login_required
def jobs_list():
    jobs = Job.query.all()
    employees = Employee.query.all()

    # if jobs:
    return render_template('jobs_list.html', title='Jobs', jobs=jobs, employees=employees)


@app.route('/job/new', methods=['GET', 'POST'])
@login_required
def add_job():
    title = request.form.get('title')
    description = request.form.get('description')

    already_exists = Job.query.filter_by(title=title).first()
    # TODO: Staviti poruku ako postoji posao
    if not already_exists:
        job = Job(title=title, description=description)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('jobs_list'))


@app.route('/job/<int:job_id>/update', methods=['POST'])
@login_required
def update_job(job_id):
    job = Job.query.get_or_404(job_id)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        job.title = title
        job.description = description
        db.session.commit()
        return redirect(url_for('jobs_list'))


@app.route('/job/<int:job_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)

    db.session.delete(job)
    db.session.commit()

    return redirect(url_for('jobs_list'))


# TODO: Staviti za brisanje radnika sa odredjenog posla (modal za poslove - Workers dugme)
@app.route('/employee/<int:job_id>/<int:employee_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_from_job(job_id, employee_id):
    # TODO: Videti sto nece da brise (ne reaguje na dugme)
    # get job and employee
    job = Job.query.get_or_404(job_id)
    employee = Employee.query.get_or_404(employee_id)

    job.employees.remove(employee)
    db.session.commit()

    return redirect(url_for('jobs_list'))


# TODO: Staviti da preko modala za posao ide na profil radnika (kad napravim route za profil)

# ================================================================================

@app.route('/employees/<int:employee_id>', methods=['GET', 'POST'])
def profile(employee_id):
    """Employee profile"""
    employee = Employee.query.get_or_404(employee_id)

    return render_template('employee.html', employee=employee)
