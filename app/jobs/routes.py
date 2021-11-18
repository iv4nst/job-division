from flask import render_template, redirect, url_for, request
from flask_login import login_required

from app import db
from app.models import Job, Employee
from app.jobs import jobs


@jobs.route('/jobs_list', methods=['GET', 'POST'])
@login_required
def jobs_list():
    all_jobs = Job.query.all()
    all_employees = Employee.query.all()

    return render_template('jobs/jobs_list.html', title='Jobs', jobs=all_jobs, employees=all_employees)


@jobs.route('/job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def job_page(job_id):
    """Job page"""
    job = Job.query.get_or_404(job_id)
    employees = Employee.query.all()

    return render_template('jobs/job.html', job=job, employees=employees)


@jobs.route('/job/add', methods=['POST'])
@login_required
def add_job():
    title = request.form.get('title')

    already_exists = Job.query.filter_by(title=title).first()
    job = Job(title=title)

    if not already_exists:
        db.session.add(job)
        db.session.commit()
    return redirect(url_for('jobs.jobs_list'))


@jobs.route('/job/<int:job_id>/update', methods=['POST'])
@login_required
def update_job(job_id):
    job = Job.query.get_or_404(job_id)

    if request.method == 'POST':
        title = request.form.get('title')

        job.title = title
        db.session.commit()
        return redirect(url_for('jobs.jobs_list'))


@jobs.route('/job/<int:job_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)

    db.session.delete(job)
    db.session.commit()

    return redirect(url_for('jobs.jobs_list'))


@jobs.route('/job/<int:job_id>/employee/<int:employee_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_from_job(job_id, employee_id):
    # TODO: Staviti da redirektuje na pravu stranicu (posto se poziva i na stranici posla, ne samo u jobs_list)
    #   ako je pozvano na jobs_list preko tabele, onda brati na jobs_list,
    #   ako je pozvano u job_page, onda vrati na job_page
    employee = Employee.query.get_or_404(employee_id)
    job = Job.query.get_or_404(job_id)
    job.employees.remove(employee)
    # del employee.job
    db.session.commit()

    return redirect(url_for('jobs.jobs_list'))


@jobs.route('/job/<int:job_id>/employee/<int:employee_id>/quit_job', methods=['POST'])
@login_required
def quit_job(job_id, employee_id):
    # TODO: Dodati jos funkcionalnosti
    employee = Employee.query.get_or_404(employee_id)
    del employee.job
    db.session.commit()
    return redirect(url_for('jobs.job_page', job_id=job_id))


@jobs.route('/job/<int:job_id>/employee/<int:employee_id>/apply', methods=['POST'])
@login_required
def apply_for_job(job_id, employee_id):
    # TODO: Namestiti da ne moze da apply ako vec ima posao (na kraju uraditi ovo ispod) - ako ima posao, apply
    #   i nakon toga kad se odobri, promeni posao
    # TODO: Dodati funkcionalnost (da ne dodaje automatski nego da treba da se odobri)
    employee = Employee.query.get_or_404(employee_id)
    job = Job.query.get_or_404(job_id).id
    employee.set_job(job)
    db.session.commit()

    return redirect(url_for('jobs.job_page', job_id=job_id))
