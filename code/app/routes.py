from flask_login.utils import login_user, logout_user, \
                              current_user, login_required
from werkzeug.utils import secure_filename
from app import app, funcs, classes, db, recommender_instance
from flask import render_template, url_for, jsonify, request, redirect, abort, flash
import os
import json
import pandas as pd

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
    zipcode = request.args.get('a', type=int)
    df = funcs.get_hh_agencies(zipcode)
    json_df = json.loads(df.to_json(orient="split"))
    return jsonify(my_table=json_df["data"],
                   columns=[{"title": str(col)} for col in json_df["columns"]])

@app.route('/register', methods=['GET', 'POST'])
def register():
    "User registration page"
    form = classes.RegisterForm()
    user_exists = False
    agency_invalid = False
    password_invalid = False
    username_invalid = False
    if form.validate_on_submit():
        account_type = form.account_type.data
        username = form.username.data
        password = form.password.data
        matching_user_count = classes.User.query.filter_by(username=username) \
                                                .count()
        if(account_type == "agency" and not recommender_instance.check_provider_name(username)):
            agency_invalid = True
        elif(matching_user_count > 0):
            user_exists = True
        else:
            user = classes.User(username, password, account_type)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            if(user.account_type == "discharge planner"):
                return redirect(url_for('discharge'))
            else:
                return redirect(url_for('agency'))
    elif request.method == 'POST' and not form.validate():
        account_type = form.account_type.data
        username = form.username.data
        password = form.password.data
        if len(password) < 8:
            password_invalid = True
        if len(username) < 4:
            username_invalid = True

    return render_template('register.html', form=form,
                           loggedin=current_user.is_authenticated,
                           user_exists=user_exists,
                           agency_invalid=agency_invalid,
                           username_too_short=username_invalid,
                           password_too_short=password_invalid)


@app.route('/login', methods=['GET', 'POST'])
def login():
    "User login page"
    form = classes.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = classes.User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            if(user.account_type == "discharge planner"):
                return redirect(url_for('discharge'))
            else:
                return redirect(url_for('agency'))
    return render_template('login.html',
                           form=form,
                           loggedin=current_user.is_authenticated)


@app.route('/discharge', methods=['GET', 'POST'])
@login_required
def discharge():
    "Discharge planner dashboard page"
    if(current_user.account_type != "discharge planner"): abort(401)
    patient_upload_form = classes.PatientUploadForm()
    if patient_upload_form.validate_on_submit():
        file = patient_upload_form.file.data
        filename = secure_filename(file.filename)

        file.save(os.path.join('code/app/upload_temp', filename))
        path = f'code/app/upload_temp/{filename}'

        patient_info = funcs.extract_patient_info(app.instance_path,
                                                  filename, file)

        planner_username = current_user.username
        first = patient_upload_form.first.data
        last = patient_upload_form.last.data
        zipcode = patient_upload_form.zipcode.data
        services = patient_upload_form.service.data

        # Change e.g. ['1', '3', '4'] to
        # [True, False, True, True, False, False]
        boolservices = [False]*6
        for i in services:
            boolservices[int(i)-1] = True

        insurance = patient_info['insurance']
        summary = patient_info['summary']

        df = recommender_instance.filter_zipcode(zipcode)
        recommendations, df_rec = recommender_instance.recommend(df,
                                                                 boolservices,
                                                                 path)

        patient = classes.Patient(planner_username=planner_username,
                                  first=first,
                                  last=last,
                                  insurance=insurance,
                                  summary=summary,
                                  recommendations=recommendations,
                                  boolservices=boolservices,
                                  zipcode=zipcode,
                                  path=path,
                                  rec_status=["A"]*len(recommendations))

        db.session.add(patient)
        db.session.commit()
        df_rec.to_pickle(f'code/app/upload_temp/recs/{patient.id}')
        recommendations.to_pickle(f'code/app/upload_temp/dfs/{patient.id}')
        return redirect(url_for('discharge'))

    patients = classes.Patient.query. \
        filter_by(planner_username=current_user.username).all()
    table_keys, table_names = classes.Patient.get_display_columns()
    return render_template('discharge.html',
                           loggedin=current_user.is_authenticated,
                           username=current_user.username,
                           patients=patients,
                           table_keys=table_keys,
                           table_names=table_names,
                           patient_upload_form=patient_upload_form)


@app.route('/agency', methods=['GET', 'POST'])
@login_required
def agency():
    "Agency user's request dashboard"
    if(current_user.account_type != "agency"): abort(401)
    agency_requests = classes.AgencyRequest.query. \
        filter_by(agency_name=current_user.username, acknowledged=False).all()
    patients = []
    for agency_request in agency_requests:
        patient = classes.Patient.query.filter_by(id=agency_request.patient_id).first()
        patients += [{
            'request_id': agency_request.id,
            'insurance': patient.insurance,
            'summary': patient.summary,
        }]
    return render_template('agency.html',
                           loggedin=current_user.is_authenticated,
                           username=current_user.username,
                           table_keys=['request_id', 'insurance', 'summary'],
                           patients=patients)



@app.route('/patient', methods=['GET', 'POST'])
@login_required
def patient():
    "Discharge planner's patient-recommendations dashboard"
    

    if(current_user.account_type != "discharge planner"): abort(401)
    id = request.args.get('id', type=int)
    patient = classes.Patient.query.filter_by(id=id).first()
    if(patient.planner_username != current_user.username):
        abort(401)

    df = recommender_instance.filter_zipcode(patient.zipcode)
    if(os.path.exists(f'code/app/upload_temp/recs/{patient.id}')):
        df_rec = pd.read_pickle(f'code/app/upload_temp/recs/{patient.id}')
    else:
        _, df_rec = recommender_instance.recommend(df,
                                                patient.boolservices,
                                                patient.path)
        
    if request.method == "POST":
        if len(list(request.form.keys())) != 4:
            print('Error with number of agencies selected')
        else:
            resulting_agencies = list(request.form.keys())[:-1]
            agency_df = pd.read_pickle(f'code/app/upload_temp/dfs/{patient.id}')
            agency_df['preventable_readmission'] = round(agency_df['preventable_readmission']/2,2)
            df3 = agency_df[agency_df.name.isin(resulting_agencies)]
            patient_name = 'ENTER NAME'

            names = df3.name.tolist()
            name1 = names[0]
            name2 = names[1]
            name3 = names[2]

            daily_activities = ['name', 'better_bathing', 
                                'better_getting_in_bed', 'better_moving']

            treating_symptoms = ['name', 'improve_breathing',
                                 'improve_wounds', 'changed_skin']

            # daily activities
            daily1 = df3[daily_activities].iloc[2].values[1:].tolist()
            daily2 = df3[daily_activities].iloc[1].values[1:].tolist()
            daily3 = df3[:3][daily_activities].iloc[0].values[1:].tolist()

            # daily activities
            symp1 = df3[treating_symptoms].iloc[2].values[1:].tolist()
            symp2 = df3[treating_symptoms].iloc[1].values[1:].tolist()
            symp3 = df3[treating_symptoms].iloc[0].values[1:].tolist()

            # preventing harm
            fall1, fall2, fall3 = funcs.return_agency_data(df3, 'checked_falling')
            depr1, depr2, depr3 = funcs.return_agency_data(df3, 'checked_depression')
            pneu1, pneu2, pneu3 = funcs.return_agency_data(df3, 'checked_pneumonia')
            flu1, flu2, flu3 = funcs.return_agency_data(df3, 'checked_flu')

            # teaching patients
            med1, med2, med3 = funcs.return_agency_data(df3, 'taught_meds')
            tmed1, tmed2, tmed3 = funcs.return_agency_data(df3, 'timely_address_meds')
            diab1, diab2, diab3 = funcs.return_agency_data(df3, 'diabetes_foot')

            # general
            score1, score2, score3 = funcs.return_agency_data(df3, 'score')
            time1, time2, time3 = funcs.return_agency_data(df3, 'timely_manner')
            ppr1, ppr2, ppr3 = funcs.return_agency_data(df3, 'preventable_readmission')
            dtc1, dtc2, dtc3 = funcs.return_agency_data(df3, 'discharge_community')
            er1, er2, er3 = funcs.return_agency_data(df3, 'ER')
            adm1, adm2, adm3 = funcs.return_agency_data(df3, 'readmitted')

            return render_template("dashboard.html", 
                                   patient_name = patient_name,
                                   agency_names = json.dumps(names),
                                   all_scores = json.dumps(df3.score.tolist()),
                                   daily1 = json.dumps(daily1), daily2 = json.dumps(daily2),
                                   daily3 = json.dumps(daily3), name1 = json.dumps(name1),
                                   name2 = json.dumps(name2), name3 = json.dumps(name3),
                                   symp1 = json.dumps(symp1), symp2 = json.dumps(symp2),
                                   symp3 = json.dumps(symp3), score1 = json.dumps(score1),
                                   score2 = json.dumps(score2), score3 = json.dumps(score3),
                                   time1 = json.dumps(time1), time2 = json.dumps(time2),
                                   time3 = json.dumps(time3), fall1 = json.dumps(fall1),
                                   fall2 = json.dumps(fall2), fall3 = json.dumps(fall3),
                                   depr1 = json.dumps(depr1), depr2 = json.dumps(depr2),
                                   depr3 = json.dumps(depr3), pneu1 = json.dumps(pneu1),
                                   pneu2 = json.dumps(pneu2), pneu3 = json.dumps(pneu3),
                                   flu1 = json.dumps(flu1), flu2 = json.dumps(flu2),
                                   flu3 = json.dumps(flu3), med1 = json.dumps(med1),
                                   med2 = json.dumps(med2), med3 = json.dumps(med3),
                                   tmed1 = json.dumps(tmed1), tmed2 = json.dumps(tmed2),
                                   tmed3 = json.dumps(tmed3), diab1 = json.dumps(diab1),
                                   diab2 = json.dumps(diab2), diab3 = json.dumps(diab3),
                                   dtc1 = json.dumps(dtc1), dtc2 = json.dumps(dtc2),
                                   dtc3 = json.dumps(dtc3), er1 = json.dumps(er1),
                                   er2 = json.dumps(er2), er3 = json.dumps(er3),
                                   adm1 = json.dumps(adm1), adm2 = json.dumps(adm2),
                                   adm3 = json.dumps(adm3), ppr1 = json.dumps(ppr1),
                                   ppr2 = json.dumps(ppr2), ppr3 = json.dumps(ppr3))

    rec_status = patient.rec_status
    df_available, df_requested, df_confirmed, df_denied, df_removed = df_rec.loc[[e == "A" for e in rec_status]],\
                                                                      df_rec.loc[[e == "W" for e in rec_status]],\
                                                                      df_rec.loc[[e == "C" for e in rec_status]],\
                                                                      df_rec.loc[[e == "D" for e in rec_status]],\
                                                                      df_rec.loc[[e == "R" for e in rec_status]]
    # Manipulating boolean services
    services = ['nursing care', 'physical therapy', 'occupational therapy', 'speech therapy', 'medical social services', 'home health aide']
    specific_services = [services[i] for i,b in enumerate(patient.boolservices) if b]

    # Cleaner columns
    clean_dict =  {'rank' : 'Rank',
                   'name' : 'Name',
                   'ppr' : '',
                   'dtc' : '',
                   'falling' : '',
                   'depression' : '',
                   'flu' : '',
                   'pneumonia' : '',
                   'diabetes' : '',
                   'moving' : '',
                   'getting_in_bed' : '',
                   'bathing' : '',
                   'breathing' : '',
                   'wounds' : '',
                   'skin_integrity' : ''}

#     df_rec.columns

    return render_template('patient.html',
                           loggedin=current_user.is_authenticated,
                           patient=patient,
                           columns=df_rec.columns,
                           data_available=df_available.values,
                           data_requested=df_requested.values,
                           data_confirmed=df_confirmed.values,
                           data_denied=df_denied.values,
                           data_removed=df_removed.values,
                           specific_services=specific_services)


@app.route('/_change_rec_status', methods=['POST'])
@login_required
def change_rec_status():
    "Endpoint for changing the status of a recommendation"
    if request.method == "POST":
        patient_id = request.form['patient_id']
        patient = classes.Patient.query.filter_by(id=patient_id).first()
        if(patient.planner_username != current_user.username):
            abort(401)
        idx = int(request.form['idx'])
        status = request.form['status']
        patient.update_rec_status(idx, status)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/_request_rec', methods=['POST'])
@login_required
def request_rec():
    "Endpoint for adding a new agency request"
    if request.method == "POST":
        patient_id = request.form['patient_id']
        patient = classes.Patient.query.filter_by(id=patient_id).first()
        if(patient.planner_username != current_user.username):
            abort(401)
        idx = int(request.form['idx'])
        patient.update_rec_status(idx, "W")
        agency_request = classes.AgencyRequest(patient_id=patient_id, planner_username=patient.planner_username, agency_name=patient.recommendations[idx])
        db.session.add(agency_request)
        db.session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/_remove_patient', methods=['POST'])
@login_required
def remove_patient():
    "Endpoint for deleting a patient, performed by discharge planner"
    if request.method == "POST":
        id = request.form['id']
        patient = classes.Patient.query.filter_by(id=id).first()
        if(patient.planner_username != current_user.username):
            abort(401)
        db.session.delete(patient)
        db.session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/_respond_request', methods=['POST'])
@login_required
def respond_request():
    "Endpoint for responding to recommendation, performed by agency"
    if request.method == "POST":
        request_id = request.form['request_id']
        status = request.form['status']
        agency_request = classes.AgencyRequest.query.filter_by(id=request_id).first()
        if(agency_request.agency_name != current_user.username):
            abort(401)
        agency_request.acknowledge()
        patient = classes.Patient.query.filter_by(id=agency_request.patient_id).first()
        rec_idx = 0
        for i,rec in enumerate(patient.recommendations):
            if(rec == current_user.username):
                rec_idx = i
                break
        patient.update_rec_status(rec_idx, status)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    username = current_user.username
    logout_user()
    return render_template('logout.html',
                           loggedin=current_user.is_authenticated,
                           username=username)
