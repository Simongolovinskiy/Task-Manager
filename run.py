from flask import Flask, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from task_manage import create_app, database


app = create_app()
# username_db, password_db = ('simon', '123')


if __name__ == '__main__':
    with app.app_context():
        database.create_all()
        app.run(debug=True, port=5000)

