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


@jobs.route('/job/new', methods=['GET', 'POST'])
@login_required
def add_job():
    # TODO: Staviti formu kao login

    title = request.form.get('title')
    description = request.form.get('description')

    already_exists = Job.query.filter_by(title=title).first()
    # TODO: Staviti poruku ako postoji posao
    if not already_exists:
        job = Job(title=title, description=description)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('jobs.jobs_list'))


@jobs.route('/job/<int:job_id>/update', methods=['POST'])
@login_required
def update_job(job_id):
    job = Job.query.get_or_404(job_id)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        job.title = title
        job.description = description
        db.session.commit()
        return redirect(url_for('jobs.jobs_list'))


@jobs.route('/job/<int:job_id>/delete', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)

    db.session.delete(job)
    db.session.commit()

    return redirect(url_for('jobs.jobs_list'))


@jobs.route('/job/employee/<int:employee_id>/delete', methods=['POST'])
@login_required
def delete_from_job(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    employee.job = None
    db.session.commit()

    return redirect(url_for('jobs.jobs_list'))

# TODO: Staviti da preko modala za posao ide na profil radnika (kad napravim route za profil)
