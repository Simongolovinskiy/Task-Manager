import os
import shutil

import sqlalchemy.exc

from task.utils import register_user_avatar
from task_manage.forms import LoginForm, RegistrationForm, UpdateAccountForm
from task_manage import bcrypt, database
from models import check_password_hash, User, Task

from flask import render_template, request, redirect, flash, url_for, Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from sqlalchemy import or_
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        database.session.add(user)
        database.session.commit()
        flash('Account successfully created. You can redirect to log into your account.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form, title='Registration', legend='Registration')


@main.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit:
        user = User.query.filter(or_(User.username == form.username.data, User.email == form.email.data)).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.account'))
        else:
            flash('Failed auth. Check your login or password', 'danger')
    return render_template('login.html', form=form, title='Login', legend='Enter')


@main.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    user = User.query.filter_by(username=current_user.username).first()
    users = User.query.all()
    tasks = Task.query.all()

    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    if form.validate_on_submit():
        old_path = os.path.join(os.getcwd(), f'task_manage/static/avatars/{user.username}')
        new_path = os.path.join(os.getcwd(), f'task_manage/static/avatars/{form.username.data}')
        os.rename(old_path, new_path)
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.avatar.data:
            current_user.img_file = register_user_avatar(form.avatar.data)

        database.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.account'))

    image_file = url_for('static', filename=f'avatars/{current_user.username}/{current_user.img_file}')
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form,
                           users=users, tasks=tasks)

@main.route('/user_delete/<string:username>', methods=['GET', 'POST'])
@login_required
def delete_user(username):
    try:
        user = User.query.filter_by(username=username).first_or_404()
        if user and user.id == 1:
            database.session.delete(user)
            database.session.commit()
            full_path = os.path.join(os.getcwd(), f'/task_manage/static/avatars/{user.username}')
        shutil.rmtree(full_path)

        flash(f'User {username} has been removed.', 'info')
        return redirect(url_for('main.account'))

    except sqlalchemy.exc.IntegrityError:

        flash(f'User {username} has  unfinished tasks.', 'warning')
        return redirect(url_for('main.account'))

    except FileNotFoundError:
        return redirect(url_for('main.account'))

@main.route('/logout')
def logout():
    current_user.last_seen = datetime.now()
    database.session.commit()
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/')
def home_page():
    return render_template('main.index')\



@main.route('/html_page')
def html_page():
    return render_template('html_page.html')


@main.route('/css_page')
def css_page():
    return render_template('css_page.html')


@main.route('/js_page')
def js_page():
    return render_template('js_page.html')


@main.route('/python_page')
def python_page():
    return render_template('python_page.html')


@main.route('/flask_page')
def flask_page():
    return render_template('flask_page.html')


@main.route('/django_page')
def django_page():
    return render_template('django_page.html')


