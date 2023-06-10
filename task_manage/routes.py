import flask_bcrypt
from flask import render_template, request, redirect, flash, url_for, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from models import check_password_hash, User
from task_manage.forms import LoginForm, RegistrationForm
from task_manage import bcrypt, database
import os
import shutil


main = Blueprint('main', __name__)
# users = Blueprint('user', __name__)


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
        full_path = os.path.join(os.getcwd(), 'main/static', 'profile_pictures', user.username)
        if not os.path.exists(full_path):
            os.mkdir(full_path)

        shutil.copy(f'{os.getcwd()}/blog/static/profile_pictures/default.jpg', full_path)
        flash('Account successfully created. You can redirect to log into your account.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form, title='Registration', legend='Registration')


@main.route('/')
def index():
    users = User.query.all()
    return render_template('base.html', users=users)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
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
    return render_template('account.html', title='Account', current_user=current_user)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/')
def home_page():
    return render_template('index.html')


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

