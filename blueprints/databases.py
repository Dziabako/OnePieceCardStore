from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    version = db.Column(db.String(10))
    stock = db.Column(db.Integer)
    price = db.Column(db.Float)
    image = db.Column(db.String(250))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, default=False)
    password = db.Column(db.String(50), nullable=False, default=False)
    name = db.Column(db.String(25))
    adress = db.Column(db.String(75))
    city = db.Column(db.String(20))
    zipcode = db.Column(db.Integer)
    country = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, nullable=False, default=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(25))
    adress = db.Column(db.String(75))
    city = db.Column(db.String(20))
    zipcode = db.Column(db.Integer)
    country = db.Column(db.String(20))
    total_price = db.Column(db.Float)
    order_number = db.Column(db.String(32))


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)

    order = db.relationship('Order', backref='order_items')
    card = db.relationship('Card')
