from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config.from_pyfile("config.cfg")
db = SQLAlchemy(app)
app.app_context().push()


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    version = db.Column(db.String(10))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    image = db.Column(db.String(250))


class CardForm(FlaskForm):
    name = StringField("Name")
    version = StringField("Version")
    quantity = IntegerField("Quantity")
    price = FloatField("Price")
    image = StringField()

# db.create_all()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_card", methods=["GET", "POST"])
def add_card():
    form = CardForm()

    if form.validate_on_submit():
        new_card = Card()
        # populate object with the same labels from form to database
        form.populate_obj(new_card)
        db.session.add(new_card)
        db.session.commit()

        flash("Added new card to database") 

        return render_template("index.html")

    
    return render_template("add_card.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
