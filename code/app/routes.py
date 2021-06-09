from app import app, funcs
from flask import render_template, url_for, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange
import json


class StringForm(FlaskForm):
    "Class for a string field form"
    field = StringField('name', validators=[DataRequired()])


class MiniZipForm(FlaskForm):
    "Form for zipcode input displayed in index.html"
    field = IntegerField(label="Zipcode")


@app.route('/')
@app.route('/index')
def index():
    "Home Page."
    return render_template('index.html')


@app.route('/zipcode_search')
def zipcode_search():
    return render_template('zipcode.html')


@app.route('/_get_table', methods=['GET', 'POST'])
def get_table():
    zipcode = request.args.get('a', type=int)
    df = funcs.get_hh_agencies(zipcode)
    json_df = json.loads(df.to_json(orient="split"))
    return jsonify(my_table=json_df["data"],
                   columns=[{"title": str(col)} for col in json_df["columns"]])
