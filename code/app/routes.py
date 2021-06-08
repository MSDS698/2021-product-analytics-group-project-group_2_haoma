from app import app, funcs
from flask import render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange


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


@app.route('/zipcode_search', methods=['GET', 'POST'])
def zipcode_search():
    "Page for finding Home Health agencies in given zipcode."
    form = StringForm()
    if form.validate_on_submit():
        zipcode = form.data['field']
        df = funcs.get_hh_agencies(zipcode)

        return render_template('zipcode.html',
                               form=form,
                               zipcode=zipcode,
                               entries=[df.to_html(
                                   classes=["table-hover-center"])])

    return render_template('zipcode.html', form=form)
