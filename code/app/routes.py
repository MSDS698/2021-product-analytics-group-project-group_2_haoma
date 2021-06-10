from flask_login.utils import login_user, logout_user, current_user, login_required
from app import app, funcs, classes, db
from flask import render_template, url_for, jsonify, request, redirect
import json

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = classes.RegisterForm()
    user_exists = False
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        matching_user_count = classes.User.query.filter_by(username=username).count()
        if(matching_user_count == 0):
            user = classes.User(username, password)
            db.session.add(user)
            db.session.commit()
            # add auto login on register
            return redirect(url_for('discharge'))
        else:
            user_exists = True
    return render_template('register.html', form=form, user_exists=user_exists)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = classes.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = classes.User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('discharge'))
    return render_template('login.html', form=form)

@app.route('/discharge', methods=['GET', 'POST'])
@login_required
def discharge():
    return render_template('discharge.html', username=current_user.username)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    username = current_user.username
    logout_user()
    return render_template('logout.html', username=username)