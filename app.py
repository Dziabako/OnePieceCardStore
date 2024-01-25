from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_pyfile("config.cfg")
app.app_context().push()

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
