import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app import recommender
from flask_login import LoginManager
import boto3

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
db.create_all()
db.session.commit()

login_manager = LoginManager()
login_manager.init_app(app)

if(os.getenv("PYTHON_ENV") == "dev"):
    s3 = boto3.client(
        's3',
        region_name='us-west-2',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
else:
    s3 = boto3.client(
        's3',
        region_name='us-west-2'
    )

recommender_instance = recommender.Recommender()

from app import classes
from app import routes