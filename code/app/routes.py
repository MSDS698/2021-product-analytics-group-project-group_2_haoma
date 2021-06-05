import pandas as pd
from app import app
from flask import render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

HH_DATA_URL = "https://data.cms.gov/provider-data/sites/default/files/resources/1ee6a6e80907bf13661aa2f099415fcd_1620794404/HH_Provider_Oct2020.csv"

class StringForm(FlaskForm):
	"Class for a string field form"
	field = StringField('name', validators=[DataRequired()])

@app.route('/')
@app.route('/index')
def index():
	"Home Page."
	return render_template('index.html')

@app.route('/zipcode_search', methods=['GET','POST'])
def zipcode_search():
	"Page for finding Home Health agencies in given zipcode."
	form = StringForm()
	if form.validate_on_submit():
		zipcode = form.data['field']
		df = pd.read_csv(HH_DATA_URL)
		hh_data = df.loc[df.ZIP == int(zipcode), 'Provider Name']

		return render_template('zipcode.html', form=form, zipcode=zipcode, hh_data=hh_data)

	return render_template('zipcode.html', form=form)