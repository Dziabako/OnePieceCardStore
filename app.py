from flask import Flask
from blueprints.decorators import login_manager
from blueprints.databases import db
from blueprints.main import main
from blueprints.cards import cards
from blueprints.basket import basket
from blueprints.users import users
from blueprints.admin import admin


app = Flask(__name__)
app.config.from_pyfile("config.cfg")
app.app_context().push()


# @login_manager.user_loader
# def load_user(id):
#     return User.query.filter(User.id == id).first()

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(main)
app.register_blueprint(cards)
app.register_blueprint(basket)
app.register_blueprint(users)
app.register_blueprint(admin)
app.app_context()


if __name__ == "__main__":
    app.run(debug=True)
