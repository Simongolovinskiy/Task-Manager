from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, FileField
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
    submit = SubmitField('Create')
