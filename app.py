from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile("config.cfg")
app.app_context().push()

db = SQLAlchemy(app)
