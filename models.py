from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin
from task_manage import database, login_manager, bcrypt
from task.utils import register_user_avatar
import os
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    __tablename__ = 'user'

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(35), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    img_file = database.Column(database.String(255), nullable=False, default='default.jpg')
    password = database.Column(database.String(60), nullable=False)
    last_seen = database.Column(database.DateTime)
    avatar = database.relationship('Task', backref='user', lazy=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, bcrypt.generate_password_hash(password).decode('utf-8'))

    def __repr__(self):
        return f'User({self.id}, {self.username}, {self.email}, {self.password}, {self.img_file})'


class Task(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(35), unique=True, nullable=False)
    contain = database.Column(database.String(500), unique=False, nullable=False)
    report = database.Column(database.String(30), nullable=False, default='default.jpg')
    #lead = database.Column(database.String(30), nullable=False)
    task_date = database.Column(database.DateTime)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'User({self.title}, {self.task_date}, {self.report})'
