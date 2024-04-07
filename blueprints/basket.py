from flask import render_template, flash, redirect, url_for, request, session, Blueprint
from flask_login import login_required, current_user
from blueprints.forms import CheckoutForm
from blueprints.databases import Card, User, Order, OrderItem, db
# Module for generating random uniqe strings for order numbers
import uuid


basket = Blueprint("basket", __name__)


@basket.route("/add_basket", methods=["GET", "POST"])
def add_basket():
    card_id = request.form.get("card_id")
    card = Card.query.filter(Card.id == card_id).first()
    quantity = request.form.get("quantity")
    total = float(card.price) * float(quantity)
    total = round(total, 2)

    if "basket" not in session:
        session["basket"] = []

    if card_id and quantity and request.method == "POST":
        for item in session["basket"]:
            if item["card_id"] == card.id:
                old_quantity = int(item["quantity"])
                new_quantity = int(request.form.get("quantity"))
                total_price_change = (new_quantity - old_quantity) * card.price
                item["quantity"] = new_quantity
                item["total"] += total_price_change
                flash("Quantity updated")
                card.stock = int(card.stock) + old_quantity - new_quantity
                db.session.commit()
                return redirect(url_for("index"))

        dictItems = {
            "card_id": card.id,
            "card": card.name,
            "version": card.version,
            "price": card.price,
            "quantity": quantity,
            "total": card.price * float(quantity),
            }

        session["basket"].append(dictItems)
        flash("Item has been added to basket!")
        card.stock = int(card.stock) - int(quantity)
        db.session.commit()
        print(session["basket"])
        return redirect(url_for("index"))
        

@basket.route("/basket")
def basket():
    total_price = 0

    for card in session["basket"]:
        total_price += card["total"]

    return render_template("basket.html", total_price=total_price)


@basket.route("/delete_basket/<int:card_id>")
def delete_basket(card_id):
    for item in session["basket"]:
        if item["card_id"] == card_id:
            card = Card.query.filter(Card.id == card_id).first()
            card.stock = int(card.stock) + int(item["quantity"])
            db.session.commit()
            session["basket"].remove(item)
            flash("Item has been removed from basket!")
            return redirect(url_for("basket"))


@basket.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    user = User.query.filter(User.id == current_user.id).first()
    form = CheckoutForm(obj=user)
    total_price = 0

    for card in session["basket"]:
        total_price += card["total"]

    if form.validate_on_submit():
        name = form.name.data
        adress = form.adress.data
        city = form.city.data
        zipcode = form.zipcode.data
        country = form.country.data
        user_id = current_user.id

        new_order = Order(
            user_id = user_id,
            name = name,
            adress = adress,
            city = city,
            zipcode = zipcode,
            country = country,
            total_price = total_price,
            # Generate 32 digit hex number
            order_number = uuid.uuid4().hex
        )
        db.session.add(new_order)
        db.session.commit()

        # Create OrderItem for each item in the basket
        for item in session["basket"]:
            order_item = OrderItem(
                order_id=new_order.id,
                card_id=item["card_id"],
                quantity=item["quantity"],
                total=item["total"]
            )
            db.session.add(order_item)

        db.session.commit()

        session.clear()
        flash("Order has been placed!")
        return redirect(url_for("order_confirm", order_id=new_order.id))

    return render_template("checkout.html", form=form, total_price=total_price)


@basket.route("/order_confirm/<order_id>")
def order_confirm(order_id):
    order = Order.query.filter(Order.id == order_id).first()
    return render_template("order_confirm.html", order=order)
