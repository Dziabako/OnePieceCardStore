from flask import render_template, flash, redirect, url_for, session, Blueprint
from blueprints.forms import BasketForm
from blueprints.databases import Card, db

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def index():
    
    form = BasketForm()
    all_cards = Card.query.all()
    

    return render_template("index.html", form=form, cards=all_cards)


@main.route("/session_clear")
def session_clear():
    session.clear()
    flash("Session cleared!")
    return redirect(url_for("index"))
