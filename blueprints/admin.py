from flask import render_template, redirect, url_for, Blueprint
from flask_login import login_required
from blueprints.forms import UserForm
from blueprints.databases import User, Order, db
from blueprints.decorators import admin_required


admin = Blueprint("admin", __name__)


@admin.route("/all_users")
@login_required
@admin_required
def all_users():
    users = User.query.all()

    return render_template("all_users.html", users=users)


@admin.route('/delete_user/<user_id>')
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.filter(User.id == user_id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("all_users"))


@admin.route("/edit_user/<user_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.filter(User.id == user_id).first()
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        user.email = form.email.data
        user.password = form.password.data
        user.name = form.name.data
        user.adress = form.adress.data
        user.city = form.city.data
        user.zipcode = form.zipcode.data
        user.country = form.country.data
        user.is_admin = form.is_admin.data

        db.session.commit()

        return redirect(url_for("all_users"))

    return render_template("edit_user.html", form=form, user=user)


@admin.route("/all_orders")
@login_required
@admin_required
def all_orders():
    orders = Order.query.all()

    return render_template("all_orders.html", orders=orders)


@admin.route("/order_info/<order_id>")
@login_required
def order_info(order_id):
    order = Order.query.filter(Order.id == order_id).first()
    order_items = order.order_items

    return render_template("order_info.html", order=order, order_items=order_items)


@admin.route("/delete_order/<order_id>")
@login_required
@admin_required
def delete_order(order_id):
    order = Order.query.filter(Order.id == order_id).first()
    db.session.delete(order)
    db.session.commit()

    return redirect(url_for("all_orders"))