from flask import render_template, flash, redirect, url_for, request, session
from forms import CardForm, BasketForm
from databases import Card
from app import app
from databases import db, Card


@app.route("/", methods=["GET", "POST"])
def index():
    form = BasketForm()
    all_cards = Card.query.all()

    return render_template("index.html", form=form, cards=all_cards)


### CARD FUNCTIONS ###
@app.route("/add_card", methods=["GET", "POST"])
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


@app.route("/all_cards")
def all_cards():
    cards = Card.query.all()

    return render_template("all_cards.html", cards=cards)


@app.route("/edit_card/<int:card_id>", methods=["GET", "POST"])
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


@app.route("/delete_card/<int:card_id>")
def delete_card(card_id):
    card = Card.query.filter(Card.id == card_id).first()
    db.session.delete(card)
    db.session.commit()

    return redirect(url_for("all_cards"))


@app.route("/card_display/<int:card_id>")
def card_display(card_id):
    card = Card.query.filter(Card.id == card_id).first()

    return render_template("card_display.html", card=card)


### BASKET ###
@app.route("/add_basket", methods=["GET", "POST"])
def add_basket():
    card_id = request.form.get("card_id")
    card = Card.query.filter(Card.id == card_id).first()
    quantity = request.form.get("quantity")
    total = card.price * quantity

    if card_id and quantity and request.method == "POST":
        dictItems = {card_id: {
            "card": card,
            "quantity": quantity,
            "total": total,
        }}

        if "basket" in session:
            print(session["basket"])
        else:
            session["basket"] = dictItems


if __name__ == "__main__":
    app.run(debug=True)
