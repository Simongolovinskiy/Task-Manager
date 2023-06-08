from flask import Flask, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from main import create_app, create_user


app = create_app()
# username_db, password_db = ('simon', '123')


if __name__ == '__main__':
    create_user()
    app.run(debug=True, port=5000)

