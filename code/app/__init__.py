from flask import Flask
from app import routes
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
