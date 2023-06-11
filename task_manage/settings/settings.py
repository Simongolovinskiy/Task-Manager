import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'))


SECRET_KEY = os.urandom(36)
SQLALCHEMY_DATABASE_URI = f"{os.environ.get('SQLALCHEMY_DATABASE_URI')}?check_same_thread=False"
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

