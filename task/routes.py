from flask import Blueprint, flash, render_template, url_for
from task.forms import TaskForm
from models import Task
from flask_login import current_user, login_required
from task.utils import save_report_task
from task_manage import database


task = Blueprint('task', __name__)


@task.route('/tasks/create', methods=['GET', 'POST'])
@login_required
def add_task():
    myform = TaskForm()
    if myform.validate_on_submit():
        newtask = Task(title=myform.title.data, contain=myform.contain.data,
                       report=myform.report.data, lead=current_user)
        report_file = save_report_task(myform.report.data)
        newtask.report = report_file
        database.session.add(newtask)
        database.session.commit()
        flash('You are successfully '
              'upload the report to commit.')
        return render_template('index.html')
    #avatar = url_for('static', filename=f'reports/{current_user.username}/report/{current_user.avatar}',)
    return render_template('add_task.html', title='New Task',
                           form=myform)


