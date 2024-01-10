from app import db


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    version = db.Column(db.String(10))
    stock = db.Column(db.Integer)
    price = db.Column(db.Float)
    image = db.Column(db.String(250))
