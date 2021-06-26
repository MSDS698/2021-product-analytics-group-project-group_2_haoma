import datetime

from flask.app import Flask
from flask_login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, IntegerField, SubmitField, \
                    PasswordField, SelectMultipleField, \
                    SelectField, widgets
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
    account_type = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password, account_type):
        self.username = username
        self.set_password(password)
        self.account_type = account_type

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Patient(db.Model):
    "Class for the patients table"
    __tablename__ = "patient"
    __table_args__ = {"schema": "public"}
    display_columns = ["id", "first", "last", "referral_date", "insurance"]
    id = db.Column(db.Integer, primary_key=True)
    planner_username = db.Column(db.String(100), nullable=False)
    first = db.Column(db.String(100), nullable=False)
    last = db.Column(db.String(100), nullable=False)
    referral_date = db.Column(db.Date(), default=datetime.datetime.utcnow)
    insurance = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text(), nullable=False)
    recommendations = db.Column(db.ARRAY(db.String(100)))
    rec_status = db.Column(db.ARRAY(db.String(1))) # "A" = available, "R" = removed, "C" = HHA confirmed, "D" = HHA denied, "W" = waiting for HHA confirmd
    
    boolservices = db.Column(db.ARRAY(db.Boolean), nullable = False)
    zipcode = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(100), nullable=False)
    matched = db.Column(db.Boolean(), nullable=False)
    agency_requests = db.relationship('AgencyRequest', backref='patient', lazy=True)
                          
        
    def get_column_names():
        names = []
        for k in Patient.__table__.columns:
            names += [" ".join(k.name.split("_")).title()]
        return names

    def get_display_columns():
        names = []
        for k in Patient.display_columns:
            names += [" ".join(k.split("_")).title()]
        return Patient.display_columns, names

    def update_rec_status(self, idx=None, status=None):
        rec_status = self.rec_status.copy()
        if(idx == None):
            self.rec_status = rec_status
        else:
            rec_status[idx] = status
        db.session.commit()


class AgencyRequest(db.Model):
    "Class for the agency_request table"
    __tablename__ = "agency_request"
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('public.patient.id'), nullable=False)
    planner_username = db.Column(db.String(100), nullable=False)
    acknowledged = db.Column(db.Boolean(), default=False)
    agency_name = db.Column(db.String(100), nullable=False)

        
    def get_column_names():
        names = []
        for k in AgencyRequest.__table__.columns:
            names += [" ".join(k.name.split("_")).title()]
        return names

    def get_display_columns():
        names = []
        for k in AgencyRequest.display_columns:
            names += [" ".join(k.split("_")).title()]
        return AgencyRequest.display_columns, names

    def acknowledge(self):
        self.acknowledged = True
        db.session.commit()


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
    account_type = SelectField(label="Register as a ", choices=["discharge planner", "agency"], validators=[DataRequired()])
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
                                 choices=[('1', 'Nursing'),
                                          ('2', 'PT'),
                                          ('3', 'OT'),
                                          ('4', 'ST'),
                                          ('5', 'Social Worker'),
                                          ('6', 'CHHA')])
    file = FileField(label='Referral Form PDF', validators=[FileRequired()])
    submit = SubmitField(label='Submit')
    

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
