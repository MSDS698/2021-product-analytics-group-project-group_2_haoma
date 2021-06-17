import datetime

from flask.app import Flask
from flask_login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, IntegerField, SubmitField, PasswordField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, NumberRange, Length


class HHCare_Zipcodes(db.Model):
    "Class for the 'hhcare_zipcodes' table."
    __tablename__ = "hhcare_zipcodes"
    __table_args__ = {"schema": "public"}
    state = db.Column(db.String(2), nullable=False)
    cms_certification_number = db.Column(db.Integer,
                                         nullable=False, primary_key=True)
    zip_code = db.Column(db.Integer, nullable=False, primary_key=True)


class User(db.Model, UserMixin):
    "Class for the 'user' table."
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}
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


class Patient(db.Model):
    "Class for the patients table"
    __tablename__ = "patient"
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True)
    planner_username = db.Column(db.String(100), nullable=False)
    first = db.Column(db.String(100), nullable=False)
    last = db.Column(db.String(100), nullable=False)
    referral_date = db.Column(db.Date(), default=datetime.datetime.utcnow)
    insurance = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text(), nullable=False)
    recommendations = db.Column(db.ARRAY(db.String(100)))

    def get_column_names():
        names = []
        for k in Patient.__table__.columns:
            names += [" ".join(k.name.split("_")).title()]
        return names


class StringForm(FlaskForm):
    "Class for a string field form"
    field = StringField('name', validators=[DataRequired()])


class MiniZipForm(FlaskForm):
    "Form for zipcode input displayed in index.html"
    field = IntegerField(label="Zipcode")


class RegisterForm(FlaskForm):
    "Form for user registration"
    username = StringField(label='Username',
                           validators=[DataRequired(), Length(min=4)])
    password = PasswordField(label='Password',
                             validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label='Register')


class LoginForm(FlaskForm):
    "Form for user login"
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')
    
    
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class PatientUploadForm(FlaskForm):
    "Form for adding a patient"
    first = StringField(label='First Name', validators=[DataRequired()])
    last = StringField(label='Last Name', validators=[DataRequired()])
    zipcode = IntegerField(label='Zip Code', validators=[DataRequired()])
    service = MultiCheckboxField('Services',
                                 choices=[('1', 'Nursing'), ('2', 'PT'), ('3', 'OT'),
                                          ('4', 'ST'), ('5', 'Social Worker'), ('6', 'CHHA')])
    file = FileField(label='Referral Form PDF', validators=[FileRequired()])
    submit = SubmitField(label='Submit')
    



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))