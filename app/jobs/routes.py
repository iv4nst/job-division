from flask import render_template, redirect, url_for, request
from flask_login import login_required

from app import db
from app.models import Job, Employee
from app.jobs import jobs


@jobs.route('/job/new', methods=['GET', 'POST'])
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
        return redirect(url_for('jobs_list'))


@jobs.route('/job/<int:job_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)

    db.session.delete(job)
    db.session.commit()

    return redirect(url_for('jobs_list'))


# TODO: Staviti za brisanje radnika sa odredjenog posla (modal za poslove - Workers dugme)
@jobs.route('/employee/<int:job_id>/<int:employee_id>/delete', methods=['POST', 'GET'])
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
