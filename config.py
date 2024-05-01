import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

