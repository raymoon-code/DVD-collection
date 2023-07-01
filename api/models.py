from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default = func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150) )
    notes = db.relationship('Note')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    opening = db.Column(db.Text)
    product_ids = db.Column(db.String(100))
    conclusion = db.Column(db.Text)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    amazon_link = db.Column(db.String(200))

class DVD(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    running_time = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    __table_args__ = (
        CheckConstraint('id >= 1'),
        CheckConstraint('id <= 100'),
    )