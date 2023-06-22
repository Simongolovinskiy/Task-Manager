from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField
from werkzeug.datastructures import FileStorage
from wtforms.validators import DataRequired
from task_manage import database


class TaskForm(FlaskForm):
    title = StringField('Header', validators=[DataRequired()])
    contain = TextAreaField('Task', validators=[DataRequired()])
    report = FileField('Execution Report', validators=[FileAllowed(['pdf', 'jpg',
                                                                     'png', 'word'])])
    submit = SubmitField('Create')


class TaskUpdate(FlaskForm):
    title = StringField('Header', validators=[DataRequired()])
    contain = TextAreaField('Task', validators=[DataRequired()])
    report = FileField('Execution Report', validators=[FileAllowed(['pdf', 'jpg',
                                                                     'png', 'word'])])
    submit = SubmitField('Commit')


class AdminTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    contain = TextAreaField('Content', validators=[DataRequired()])
    report = FileField('Report')
    user = SelectField('Assign to User', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create')