import os

from datetime import datetime

from task.forms import TaskForm
from models import Task
from task.utils import save_report_task
from task_manage import database

from flask import Blueprint, flash, render_template,  url_for,  request
from flask_login import current_user, login_required
from flask import send_from_directory, current_app

from werkzeug.exceptions import NotFound

task = Blueprint('task', __name__)


@task.route('/tasks/create', methods=['GET', 'POST'])
@login_required
def add_task():
    myform = TaskForm()
    if myform.validate_on_submit():
        newtask = Task(title=myform.title.data, contain=myform.contain.data,
                       report=myform.report.data, task_date=datetime.now(), user_id=current_user.id)
        report_file = save_report_task(myform.report.data)
        newtask.report = report_file
        database.session.add(newtask)
        database.session.commit()
        flash('You are successfully '
              'upload the report to commit.')
        return render_template('index.html')
    avatar = url_for('static', filename=f'reports/{current_user.username}/avatars/{current_user.avatar}',)
    return render_template('add_task.html', title='New Task',
                           form=myform, image_file=avatar)


@task.route('/tasks', methods=['GET', 'POST'])
@login_required
def show_tasks():
    mytasks = None
    mytask = Task.query.get(current_user.id)
    if mytask:
        page = request.args.get('page', 1, type=int)
        mytasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.task_date.desc()).paginate(page=page, per_page=3)
    return render_template('show_tasks.html', tasks=mytasks)


@task.route('/download/<int:task_id>/<path:filename>', methods=['GET'])
@login_required
def download_file(task_id, filename):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        raise NotFound()

    directory = os.path.join(current_app.root_path, 'static', f'reports/{current_user.username}/{current_user.username}_report')
    file_path = os.path.join(directory, filename)

    if os.path.isfile(file_path):
        file_name = os.path.basename(file_path)
        return send_from_directory(directory, file_name, as_attachment=True)
    else:
        raise NotFound()









