from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    articles = db.relationship('Article', backref='author', lazy=True)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Message(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    message = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"Message: <{self.subject}>"