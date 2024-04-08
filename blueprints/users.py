from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from blueprints.forms import UserForm, LoginForm
from blueprints.databases import User, Order, db


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    form = UserForm()

    if form.validate_on_submit():
        email = form.email.data
        email_check = form.email_check.data
        password = form.password.data
        password_check = form.password_check.data
        name = form.name.data
        adress = form.adress.data
        city = form.city.data
        zipcode = form.zipcode.data
        country = form.country.data

        if User.query.filter(User.email == email).first() or User.query.filter(User.name == name).first():
            flash("User already exist! Login first!")
            return redirect(url_for("login"))
        
        if password == password_check and email == email_check:
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


@users.route("/login", methods=["GET", "POST"])
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
            flash("Logged In")
            return redirect(url_for('main.index'))

    return render_template("login.html", form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged OUT!")
    return redirect(url_for("main.index"))


@users.route("/account_details/<user_id>")
@login_required
def account_details(user_id):
    user = User.query.filter(User.id == user_id).first()
    user_orders = Order.query.filter(Order.user_id == user_id).all()

    return render_template("account_details.html", user=user, user_orders=user_orders)


@users.route("/user_edit/<user_id>", methods=["GET", "POST"])
def user_edit(user_id):
    user = User.query.filter(User.id == user_id).first()
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        new_email = form.email.data
        if new_email != user.email:
            user.email = new_email
            db.session.commit()

        new_password = form.password.data
        if not check_password_hash(user.password, new_password):
            user.password = generate_password_hash(new_password)
            db.session.commit()

        new_name = form.name.data
        if new_name != user.name:
            user.name = new_name
            db.session.commit()
        
        new_adress = form.adress.data
        if new_adress != user.adress:
            user.adress = new_adress
            db.session.commit()
        
        new_city = form.city.data
        if new_city != user.city:
            user.city = new_city
            db.session.commit()

        new_zipcode = form.zipcode.data
        if new_zipcode != user.zipcode:
            user.zipcode = new_zipcode
            db.session.commit()

        new_country = form.country.data
        if new_country != user.country:
            user.country = new_country
            db.session.commit()
        
        flash("User data has been changed!")

        return redirect(url_for("account_details", user_id=user.id))

    return render_template("user_edit.html", form=form, user=user)


@users.route("/order_info/<order_id>")
@login_required
def order_info(order_id):
    order = Order.query.filter(Order.id == order_id).first()
    order_items = order.order_items

    return render_template("order_info.html", order=order, order_items=order_items)
