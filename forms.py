from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired


class CardForm(FlaskForm):
    name = StringField("Name")
    version = StringField("Version")
    stock = IntegerField("Stock")
    price = FloatField("Price")
    image = StringField()


class BasketForm(FlaskForm):
    quantity = IntegerField("Quantity")


class UserForm(FlaskForm):
    email = StringField("Email: ")
    password = StringField("Password: ")
    name = StringField("Name: ")
    adress = StringField("Adress: ")
    city = StringField("City: ")
    zipcode = IntegerField("ZipCode: ")
    country = StringField("Country: ")


class LoginForm(FlaskForm):
    email = StringField("Email: ")
    password = StringField("Password: ")
