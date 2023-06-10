from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User
from flask import flash


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=15)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Enter')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data)
        if user:
            flash('That username is already taken. '
                  'Choose another one, please', 'danger')
            raise ValidationError('That username is already taken.')


    def validate_email(self, email):
        myemail = User.query.filter_by(email=email.data).first()
        if myemail:
            flash('That e-mail is already taken. '
                  'Choose another one, please', 'danger')
            raise ValidationError('That email is already taken.')


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Stay logged')
    submit = SubmitField('Login')
    