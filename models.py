from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin
from task_manage import database, login_manager, bcrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    __tablename__ = 'user'

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(35), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    img_file = database.Column(database.String(20), nullable=False, default='default.jpg')
    password = database.Column(database.String(60), nullable=False)
    #tasks = database.relationship('Task', backref='for me', lazy=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, bcrypt.generate_password_hash(password).decode('utf-8'))

    def __repr__(self):
        return f'User({self.id}, {self.username}, {self.email}, {self.password}, {self.img_file})'



