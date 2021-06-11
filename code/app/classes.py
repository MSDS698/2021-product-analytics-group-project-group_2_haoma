from flask_login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length

class User(db.Model, UserMixin):
    __table_name__ = "user"
    schema = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class StringForm(FlaskForm):
    "Class for a string field form"
    field = StringField('name', validators=[DataRequired()])

class MiniZipForm(FlaskForm):
    "Form for zipcode input displayed in index.html"
    field = IntegerField(label="Zipcode")

class RegisterForm(FlaskForm):
    "Form for user registration"
    username = StringField(label='Username', validators=[DataRequired(), Length(min=4)])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label='Register')

class LoginForm(FlaskForm):
    "Form for user login"
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))