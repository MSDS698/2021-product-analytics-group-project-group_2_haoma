from flask_login.utils import login_user, logout_user, \
                              current_user, login_required
from werkzeug.utils import secure_filename
from app import app, funcs, classes, db, recommender_instance
from flask import render_template, url_for, jsonify, request, redirect, abort
import os
import json


@app.route('/')
@app.route('/index')
def index():
    "Home Page."
    return render_template('index.html',
                           loggedin=current_user.is_authenticated)


@app.route('/zipcode_search')
def zipcode_search():
    return render_template('zipcode.html',
                           loggedin=current_user.is_authenticated)


@app.route('/_get_table', methods=['GET', 'POST'])
def get_table():
    df_rec = request.args.get('df_rec')
    json_df = json.loads(df_rec.to_json(orient="split"))
    return jsonify(my_table=json_df["data"],
                   columns=[{"title": str(col)} for col in json_df["columns"]])


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = classes.RegisterForm()
    user_exists = False
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        matching_user_count = classes.User.query.filter_by(username=username) \
                                                .count()
        if(matching_user_count == 0):
            user = classes.User(username, password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('discharge'))
        else:
            user_exists = True
    return render_template('register.html', form=form,
                           loggedin=current_user.is_authenticated,
                           user_exists=user_exists)


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
    return render_template('login.html',
                           form=form,
                           loggedin=current_user.is_authenticated)


@app.route('/discharge', methods=['GET', 'POST'])
@login_required
def discharge():
    patient_upload_form = classes.PatientUploadForm()
    if patient_upload_form.validate_on_submit():
        file = patient_upload_form.file.data
        filename = secure_filename(file.filename)
<<<<<<< HEAD
        
        file.save(os.path.join('app/upload_temp', filename))
        path = f'app/upload_temp/{filename}'
    
=======

        file.save(os.path.join('code/app/upload_temp', filename))
        pdf_path = f'code/app/upload_temp/{filename}'

>>>>>>> 9c69a220060fa7c3da524ddbb55921007d3bf500
        patient_info = funcs.extract_patient_info(app.instance_path,
                                                  filename, file)

        planner_username = current_user.username
        first = patient_upload_form.first.data
        last = patient_upload_form.last.data
        zipcode = patient_upload_form.zipcode.data
        services = patient_upload_form.service.data
<<<<<<< HEAD
        # Change e.g. ['1', '3', '4'] to [True, False, True, True, False, False]
        boolservices = [False]*6
        for i in services:
            boolservices[int(i)-1] = True
        
        insurance = patient_info['insurance']
        summary = patient_info['summary']
        
        
        df = recommender_instance.filter_zipcode(zipcode)
        recommendations, df_rec = recommender_instance.recommend(df, boolservices, path)
        
=======
        # Change e.g. ['1', '3', '4'] to
        # [True, False, True, True, False, False]
        bool_services = [False]*6
        for i in services:
            bool_services[int(i)-1] = True

        insurance = patient_info['insurance']
        summary = patient_info['summary']

        df = recommender_instance.filter_zipcode(zipcode)
        recommendations = recommender_instance.recommend(df,
                                                         bool_services,
                                                         pdf_path)
>>>>>>> 9c69a220060fa7c3da524ddbb55921007d3bf500
        patient = classes.Patient(planner_username=planner_username,
                                  first=first,
                                  last=last,
                                  insurance=insurance,
                                  summary=summary,
                                  recommendations=recommendations,
                                  boolservices = boolservices,
                                  zipcode = zipcode,
                                  path = path)
        
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('discharge'))

    patients = classes.Patient.query. \
        filter_by(planner_username=current_user.username).all()
    return render_template('discharge.html',
                           loggedin=current_user.is_authenticated,
                           username=current_user.username,
                           patients=patients,
                           table_keys=[c.name for c in
                                       classes.Patient.__table__.columns],
                           table_names=classes.Patient.get_column_names(),
                           patient_upload_form=patient_upload_form)


@app.route('/patient', methods=['GET', 'POST'])
@login_required
def patient():
    id = request.args.get('id', type=int)
    patient = classes.Patient.query.filter_by(id=id).first()
    if(patient.planner_username != current_user.username):
        abort(401)
        
    df = recommender_instance.filter_zipcode(patient.zipcode)
    recommendations, df_rec = recommender_instance.recommend(df, 
                                                     patient.boolservices, 
                                                     patient.path)
    
    scores = recommender_instance.get_metrics(patient.recommendations,
                                              patient.summary)
    score_keys = recommender_instance.score_keys
    score_names = recommender_instance.get_column_names()
    return render_template('patient.html',
                           loggedin=current_user.is_authenticated,
                           patient=patient,
                           scores=scores,
                           score_keys=score_keys,
                           score_names=score_names,
                           data = df_rec.to_html(table_id="example"))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    username = current_user.username
    logout_user()
    return render_template('logout.html',
                           loggedin=current_user.is_authenticated,
                           username=username)
