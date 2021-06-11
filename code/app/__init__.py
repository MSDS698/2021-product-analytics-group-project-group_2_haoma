import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
db.create_all()
db.session.commit()

login_manager = LoginManager()
login_manager.init_app(app)

from app import classes
from app import routes