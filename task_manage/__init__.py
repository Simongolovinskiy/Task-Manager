from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate


database = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'You need to authorize to get access to this page.'


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings/settings.py')
    database.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, database, render_as_batch=True)
    login_manager.init_app(app)

    from task_manage.routes import main
    from task.routes import task
    # from task_manage.routes import users
    app.register_blueprint(main)
    app.register_blueprint(task)
    # app.register_blueprint(users)

    return app


app_ctx = create_app()

