from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, FloatField, BooleanField, PasswordField
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
    email = StringField("Email: ", validators=[DataRequired("Enter email")])
    email_check = StringField("Email Check: ", validators=[DataRequired("Enter email check")])
    password = PasswordField("Password: ", validators=[DataRequired("Enter password")])
    password_check = PasswordField("Password Check: ", validators=[DataRequired("Enter password check")])
    name = StringField("Name: ", validators=[DataRequired("Enter name")])
    adress = StringField("Adress: ", validators=[DataRequired("Enter adress")])
    city = StringField("City: ", validators=[DataRequired("Enter city")])
    zipcode = IntegerField("ZipCode: ", validators=[DataRequired("Enter zipcode")])
    country = StringField("Country: ", validators=[DataRequired("Enter country")])
    is_admin = BooleanField("Is admin?: ")


class LoginForm(FlaskForm):
    email = StringField("Email: ")
    password = PasswordField("Password: ")


class CheckoutForm(FlaskForm):
    name = StringField("Name: ")
    adress = StringField("Adress: ")
    city = StringField("City: ")
    zipcode = IntegerField("ZipCode: ")
    country = StringField("Country: ")
