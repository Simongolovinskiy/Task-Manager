from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


database = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings\settings.py')
    database.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from main.routes import main
    app.register_blueprint(main)

    return app


app_ctx = create_app()


def create_user():
    with app_ctx.app_context():
        from models import User

        database.drop_all()
        database.create_all()
        hashed_password = bcrypt.generate_password_hash(str('123')).decode('utf-8')
        user = User(username='Simon', email='example@mail.ru', password=hashed_password)
        database.session.add(user)
        database.session.commit()

