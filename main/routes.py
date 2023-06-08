from flask import render_template, request, redirect, flash, url_for, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from models import check_password_hash, User
from main.forms import LoginForm


main = Blueprint('main', __name__)


@main.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


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

