from app import db
from flask_login import UserMixin


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    version = db.Column(db.String(10))
    stock = db.Column(db.Integer)
    price = db.Column(db.Float)
    image = db.Column(db.String(250))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    name = db.Column(db.String(25))
    adress = db.Column(db.String(75))
    city = db.Column(db.String(20))
    zipcode = db.Column(db.Integer)
    country = db.Column(db.String(20))
