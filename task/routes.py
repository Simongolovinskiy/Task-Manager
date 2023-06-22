import os

from datetime import datetime

from task.forms import TaskForm, TaskUpdate, AdminTaskForm
from models import Task, User
from task.utils import save_report_task
from task_manage import database
from flask import Blueprint, flash, render_template,  url_for,  request, redirect
from flask_login import current_user, login_required
from flask import send_from_directory, current_app

from werkzeug.exceptions import NotFound

task = Blueprint('task', __name__)


@task.route('/tasks/create', methods=['GET', 'POST'])
@login_required
def add_task():
    if current_user.is_admin:
        myform = AdminTaskForm()
        myform.user.choices = [(user.id, user.username) for user in User.query.all()]
    else:
        myform = TaskForm()

    if myform.validate_on_submit():
        if current_user.is_admin:
            user_id = myform.user.data
        else:
            user_id = current_user.id

        newtask = Task(
            title=myform.title.data,
            contain=myform.contain.data,
            report=myform.report.data,
            task_date=datetime.now(),
            user_id=user_id
        )

        if myform.report.data:
            report_file = save_report_task(myform.report.data)
            newtask.report = report_file

        database.session.add(newtask)
        database.session.commit()

        flash('Task added successfully.', 'success')
        return redirect(url_for('task.show_tasks'))

    avatar = url_for('static', filename=f'reports/{current_user.username}/avatars/{current_user.avatar}')
    return render_template('add_task.html', title='New Task', form=myform, image_file=avatar)



@task.route('/tasks', methods=['GET', 'POST'])
@login_required
def show_tasks():
    mytasks = None
    page = request.args.get('page', 1, type=int)

    if current_user.is_admin:
        mytasks = Task.query.order_by(Task.task_date.desc()).paginate(page=page, per_page=3)
    else:
        mytasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.task_date.desc()).paginate(page=page,
                                                                                                         per_page=3)

    return render_template('show_tasks.html', tasks=mytasks)


@task.route('/download/<int:task_id>/<path:filename>', methods=['GET'])
@login_required
def download_file(task_id, filename):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        raise NotFound()

    directory = os.path.join(current_app.root_path, 'static', f'users/{current_user.username}/reports')
    file_path = os.path.join(directory, filename)

    if os.path.isfile(file_path):
        file_name = os.path.basename(file_path)
        return send_from_directory(directory, file_name, as_attachment=True)
    else:
        raise NotFound()


@task.route('/task/<int:task_id>/commit', methods=['GET', 'POST'])
def task_commit(task_id):
    task = Task.query.get(int(task_id))
    form = TaskUpdate()

    if request.method == 'GET':
        form.title.data = task.title
        form.report.data = task.report
        form.contain.data = task.contain

    if form.validate_on_submit():
        task.title = form.title.data
        task.contain = form.contain.data

        if form.report.data:
            new_report = save_report_task(form.report.data)
            task.report = new_report
        task.updated = True
        database.session.commit()
        flash('Task has been updated for check', 'success')
        return redirect(url_for('task.show_tasks'))
    return render_template('task_commit.html', legend='commit', task=task, form=form)

@task.route('/task/<int:task_id>/delete', methods=['POST'])
def task_delete(task_id):
    task = Task.query.get(int(task_id))
    if current_user.id != 1:
        if current_user.id != task.user_id:
            flash("You don't have permission to delete this task,", 'danger')
            return redirect(url_for('task.show_tasks'))
    database.session.delete(task)
    database.session.commit()
    flash('Successfully deleted task!', 'success')
    return redirect(url_for('task.show_tasks'))

