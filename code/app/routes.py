from app import application
from flask import render_template

@application.route('/')
@application.route('/index')
def index():
	return render_template('index.html')