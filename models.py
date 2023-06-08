from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin
from main import database, login_manager, bcrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    __tablename__ = 'user'

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(35), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    password = database.Column(database.String(60), nullable=False)

    def set_password(self, password, hashed_password):
        self.hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.password})'



