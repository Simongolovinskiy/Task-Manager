from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin
from task_manage import database, login_manager, bcrypt
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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
    is_admin = database.Column(database.Boolean, default=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, bcrypt.generate_password_hash(password).decode('utf-8'))

    def get_reset_token(self, expires_sec=3600):
        reset_token = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return reset_token.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        return User.query.get(user_id)
    def __repr__(self):
        return f'User({self.id}, {self.username}, {self.email}, {self.password}, {self.img_file})'


class Task(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(35), unique=True, nullable=False)
    contain = database.Column(database.String(500), unique=False, nullable=False)
    report = database.Column(database.String(255), nullable=False, default='default.jpg')
    task_date = database.Column(database.DateTime)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    updated = database.Column(database.Boolean, default=False)
    def __repr__(self):
        return f'User({self.title}, {self.task_date}, {self.report})'
