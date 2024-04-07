from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_required
from blueprints.forms import CardForm
from blueprints.databases import Card, db
from blueprints.decorators import admin_required


cards = Blueprint("cards", __name__)


@cards.route("/add_card", methods=["GET", "POST"])
@login_required
@admin_required
def add_card():
    """Adding new card to database"""
    form = CardForm()

    if form.validate_on_submit():
        new_card = Card()
        # Populate object with the same labels from form to database
        form.populate_obj(new_card)
        db.session.add(new_card)
        db.session.commit()

        flash("Added new card to database") 

        return redirect(url_for("index"))

    
    return render_template("add_card.html", form=form)


@cards.route("/all_cards")
@login_required
@admin_required
def all_cards():
    cards = Card.query.all()

    return render_template("all_cards.html", cards=cards)


@cards.route("/edit_card/<int:card_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_card(card_id):
    card = Card.query.filter(Card.id == card_id).first()
    # Attributes from card object matching form field names will be used for field values
    form = CardForm(obj=card)

    if form.validate_on_submit():
        card.name = form.name.data
        card.version = form.version.data
        card.stock = form.stock.data
        card.price = form.price.data
        card.image = form.image.data

        db.session.commit()

        flash("Succesfully updated card")

        return redirect(url_for("all_cards"))

    return render_template("edit_card.html", form=form, card=card)


@cards.route("/delete_card/<int:card_id>")
@login_required
@admin_required
def delete_card(card_id):
    card = Card.query.filter(Card.id == card_id).first()
    db.session.delete(card)
    db.session.commit()

    return redirect(url_for("all_cards"))


@cards.route("/card_display/<int:card_id>")
def card_display(card_id):
    card = Card.query.filter(Card.id == card_id).first()

    return render_template("card_display.html", card=card)