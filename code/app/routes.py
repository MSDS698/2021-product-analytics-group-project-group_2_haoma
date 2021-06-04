from app import application
from flask import render_template

@application.route('/')
@application.route('/index')
def index():
	"Home page for our application."
	return render_template('index.html')