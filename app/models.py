from . import db  # Импорт объекта db из вашего Flask-приложения
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
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)  # Adding a title column
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

class DiabetesModel(db.Model):  # Изменение наследования на db.Model
    id = db.Column(db.Integer, primary_key=True)
    pregnancies = db.Column(db.Float)
    glucose = db.Column(db.Float)
    bloodpressure = db.Column(db.Float)
    skinthickness = db.Column(db.Float)
    insulin = db.Column(db.Float)
    bmi = db.Column(db.Float)
    diabetespedigreefunction = db.Column(db.Float)
    age = db.Column(db.Float)
    probability = db.Column(db.Float)
