from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired


class CardForm(FlaskForm):
    name = StringField("Name")
    version = StringField("Version")
    stock = IntegerField("Stock")
    price = FloatField("Price")
    image = StringField()
