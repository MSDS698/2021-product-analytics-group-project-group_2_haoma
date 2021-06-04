from app import app
from flask import render_template, url_for

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')