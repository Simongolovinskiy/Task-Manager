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
    app.config.from_pyfile('settings/settings.py')
    database.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from task_manage.routes import main
    # from task_manage.routes import users
    app.register_blueprint(main)
    # app.register_blueprint(users)

    return app


app_ctx = create_app()

