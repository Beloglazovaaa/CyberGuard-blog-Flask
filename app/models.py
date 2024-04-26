from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    articles = db.relationship('Article', backref='user', passive_deletes=True)
    def __repr__(self):
        return f'User: <{self.username}>'

class Article(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
