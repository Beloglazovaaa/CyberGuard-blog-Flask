import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3307/DB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

