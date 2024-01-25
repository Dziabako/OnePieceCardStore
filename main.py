from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CardForm, BasketForm, UserForm, LoginForm
from databases import Card, User, db
from app import app, login_manager


db.create_all()
@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()


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
    total = float(card.price) * float(quantity)
    total = round(total, 2)

    if "basket" not in session:
        session["basket"] = []

    if card_id and quantity and request.method == "POST":
        dictItems = {
            "card_id": card.id,
            "card": card.name,
            "version": card.version,
            "price": card.price,
            "quantity": quantity,
            "total": total,
        }

        if "basket" in session:
            if card_id not in session["basket"]:
                session["basket"].append(dictItems)
                flash("Item has been added to basket!")
                card.stock = int(card.stock) - int(quantity)
                db.session.commit()
            else:
                new_quantity = request.form.get("quantity")
                session["basket"][card_id]["quantity"] = new_quantity
                flash("Quantity updated")
                card.stock = int(card.stock) + int(quantity)
                card.stock = int(card.stock) - int(new_quantity)
                db.session.commit()
            print(session["basket"])
            return redirect(url_for("index"))
        

@app.route("/basket")
def basket():
    total_price = 0

    for card in session["basket"]:
        total_price += card["total"]

    return render_template("basket.html", total_price=total_price)


### USERS ###
@app.route("/register", methods=["GET", "POST"])
def register():
    form = UserForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        name = form.name.data
        adress = form.adress.data
        city = form.city.data
        zipcode = form.zipcode.data
        country = form.country.data

        if User.query.filter(User.email == email).first() or User.query.filter(User.name == name).first():
            flash("User already exist! Login first!")
            return redirect(url_for("login"))
        
        hash_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        new_user = User(
            email = email,
            password = hash_password,
            name = name,
            adress = adress,
            city = city,
            zipcode = zipcode,
            country = country
        )
        db.session.add(new_user)
        db.session.commit()
        flash("User created! You can Login now!")
        return redirect(url_for("index"))
    
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter(User.email == email).first()
        
        if not user: 
            flash("That email does not exist, pleae try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Wrong password! Try again")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('index'))

    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
