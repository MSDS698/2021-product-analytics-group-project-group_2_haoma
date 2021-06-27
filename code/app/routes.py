from pkg_resources import parse_version
from app.funcs import return_agency_data
from flask_login.utils import login_user, logout_user, \
                              current_user, login_required
from werkzeug.utils import secure_filename
from app import app, funcs, classes, db, recommender_instance
from app.constants import *
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
        gender = patient_upload_form.gender.data
        age = patient_upload_form.age.data
        urgent = patient_upload_form.urgent.data
        num_readmitted = patient_upload_form.num_readmitted.data

        # Change e.g. ['1', '3', '4'] to
        # [True, False, True, True, False, False]
        boolservices = [False]*6
        for i in services:
            boolservices[int(i)-1] = True

        insurance = patient_info['insurance']
        summary = patient_info['summary']

        df = recommender_instance.filter_zipcode(zipcode)
        df_agency, df_rec = recommender_instance.recommend(df,
                                                           boolservices,
                                                           path)

        patient = classes.Patient(planner_username=planner_username,
                                  first=first,
                                  last=last,
                                  insurance=insurance,
                                  summary=summary,
                                  recommendations=df_agency.name.tolist(),
                                  boolservices=boolservices,
                                  zipcode=zipcode,
                                  age=age,
                                  urgent=urgent,
                                  gender=gender,
                                  path=path,
                                  rec_status=["A"]*20,
                                  num_readmitted=num_readmitted)

        db.session.add(patient)
        db.session.commit()
        if(not os.path.exists('code/app/upload_temp/recs')): os.mkdir('code/app/upload_temp/recs')
        if(not os.path.exists('code/app/upload_temp/dfs')): os.mkdir('code/app/upload_temp/dfs')
        df_rec.to_pickle(f'code/app/upload_temp/recs/{patient.id}')
        df_agency.to_pickle(f'code/app/upload_temp/recs/dash{patient.id}')
        return redirect(url_for('discharge'))

    elif request.method == 'POST' and not patient_upload_form.validate():
        print('Cant validate')
        planner_username = current_user.username
        first = patient_upload_form.first.data
        last = patient_upload_form.last.data
        zipcode = patient_upload_form.zipcode.data
        services = patient_upload_form.service.data
        gender = patient_upload_form.gender.data
        age = patient_upload_form.age.data
        urgent = patient_upload_form.urgent.data
        num_readmitted = patient_upload_form.num_readmitted.data
        print(planner_username)
        print(first)
        print(last)
        print(zipcode)
        print(services)
        print(gender)
        print(age)
        print(urgent)

        pass

    patients = classes.Patient.query. \
        filter_by(planner_username=current_user.username).all()
    active_patients = [p for p in patients if p.status == 'A']
    history_patients = [p for p in patients if p.status == 'M' or p.status == 'R']
    table_keys, table_names = classes.Patient.get_display_columns()
    return render_template('discharge.html',
                           loggedin=current_user.is_authenticated,
                           username=current_user.username,
                           active_patients=active_patients,
                           history_patients=history_patients,
                           table_keys=table_keys,
                           table_names=table_names,
                           patient_upload_form=patient_upload_form)


@app.route('/agency', methods=['GET', 'POST'])
@login_required
def agency():
    "Agency user's request dashboard"
    if(current_user.account_type != "agency"): abort(401)
    agency_requests = classes.AgencyRequest.query. \
        filter_by(agency_name=current_user.username).all()
    print(agency_requests)
    print("FOR:", current_user.username)
    requested_patients = []
    accepted_patients = []
    pending_patients = []
    for agency_request in agency_requests:
        patient = agency_request.patient
        patient_info = [{
            'request_id': agency_request.id,
            'insurance': patient.insurance,
            'summary': patient.summary,
            'first name': patient.first,
            'last name': patient.last,
            'age': patient.age,
            'gender': patient.gender,
            'location': patient.zipcode,
            'urgent': patient.urgent,
            'num_readmitted': patient.num_readmitted,
            'first': patient.first,
            'last': patient.last,
            'zipcode': patient.zipcode,
            'referral date': patient.referral_date
        }]
        status = patient.rec_status[[i for i,rec in enumerate(patient.recommendations) if rec == agency_request.agency_name][0]]
        print(patient_info)
        print(status)
        if(status in ['A','W']):
            requested_patients += patient_info
        elif(status == 'M'):
            accepted_patients += patient_info
        elif status == 'C':
            pending_patients += patient_info

    return render_template('agency.html',
                           loggedin=current_user.is_authenticated,
                           username=current_user.username,
                           table_keys=['request_id', 'first name', 
                                       'last name', 'age',
                                       'insurance', 'gender', 
                                       'location', 'urgent'],
                           requested_patients=requested_patients,
                           accepted_patients=accepted_patients,
                           pending_patients=pending_patients)



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
    if os.path.exists(f'code/app/upload_temp/recs/{patient.id}'):
        df_rec = pd.read_pickle(f'code/app/upload_temp/recs/{patient.id}')
        df_agency = pd.read_pickle(f'code/app/upload_temp/recs/dash{patient.id}')

    else:
        df_agency, df_rec = recommender_instance.recommend(df,
                                                patient.boolservices,
                                                patient.path)

    if request.method == "POST":
        if len(list(request.form.keys())) < 3 or len(list(request.form.keys())) > 6:
            print('Error with number of agencies selected')
        else:
            print(request.form.keys())
            resulting_agencies = list(request.form.keys())[1:]
            df_agency['preventable_readmission'] = round(df_agency['preventable_readmission']/2,2)
            df = df_agency[df_agency.name.isin(resulting_agencies)]
            patient_name = patient.first
            num_agencies = len(resulting_agencies)
            names = df.name.tolist()
            all_scores = list(map(lambda x: [x, round(100-x,2)], df.score.tolist()))
            all_timely = list(map(lambda x: [x, round(100-x,2)], df.timely_manner.tolist()))
            all_ppr = list(map(lambda x: [x, round(100-x,2)], df.preventable_readmission.tolist()))

            data = {
                'num_agencies': num_agencies,
                'patient_name': patient_name,
                'name': json.dumps(names),
                'score': json.dumps(all_scores),
                'daily': json.dumps([df[agency_df_keys['daily_activities']].iloc[i].values[1:].tolist() for i in range(num_agencies)]),
                'symptom': json.dumps([df[agency_df_keys['daily_activities']].iloc[i].values[1:].tolist() for i in range(num_agencies)]),
                'timely': json.dumps(all_timely),
                'ppr': json.dumps(all_ppr),
                'dtc': json.dumps(return_agency_data(df, agency_df_keys['dtc'])),
                'er': json.dumps(return_agency_data(df, agency_df_keys['er'])),
                'readmitted': json.dumps(return_agency_data(df, agency_df_keys['readmitted'])),
                'falling': json.dumps(return_agency_data(df, agency_df_keys['falling'])),
                'depression': json.dumps(return_agency_data(df, agency_df_keys['depression'])),
                'pneumonia': json.dumps(return_agency_data(df, agency_df_keys['pneumonia'])),
                'flu': json.dumps(return_agency_data(df, agency_df_keys['flu'])),
                'timely_med': json.dumps(return_agency_data(df, agency_df_keys['timely_med'])),
                'taught_med': json.dumps(return_agency_data(df, agency_df_keys['taught_med'])),
                'diabetes': json.dumps(return_agency_data(df, agency_df_keys['diabetes'])),
            }

            colors = {
                'colors': json.dumps(dashboard_colors),
                'bg_colors': json.dumps(background_colors)
            }

            col_first_size = 5
            col_size = 2
            if(num_agencies == 3):
                col_first_size = 4
                col_size = 2
            elif(num_agencies == 4):
                col_first_size = 4
                col_size = 2
            elif(num_agencies == 5):
                col_first_size = col_size = 2

            return render_template("dashboard.html",
                                loggedin=current_user.is_authenticated,
                                dashboard_key_order=dashboard_key_order,
                                dashboard_key_order_json=json.dumps(dashboard_key_order),
                                dashboard_chart_types=json.dumps(dashboard_chart_types),
                                dashboard_barchart_labels=json.dumps(dashboard_barchart_labels),
                                dashboard_chart_titles=json.dumps(dashboard_chart_titles),
                                dashboard_info=dashboard_info,
                                show_haoma_desc=num_agencies<4,
                                col_first_size=col_first_size,
                                col_size=col_size,
                                name_arr=names,
                                colors_arr=dashboard_colors,
                                **colors, **data)


    rec_status = patient.rec_status[:20]
    df_available, df_requested, df_confirmed, df_denied, df_removed, df_matched = df_rec.loc[[e == "A" for e in rec_status]],\
                                                                      df_rec.loc[[e == "W" for e in rec_status]],\
                                                                      df_rec.loc[[e == "C" for e in rec_status]],\
                                                                      df_rec.loc[[e == "D" for e in rec_status]],\
                                                                      df_rec.loc[[e == "R" for e in rec_status]],\
                                                                      df_rec.loc[[e == "M" for e in rec_status]]
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
                           columns=df_rec.columns.values,
                           data_available=df_available.values,
                           data_requested=df_requested.values,
                           data_confirmed=df_confirmed.values,
                           data_denied=df_denied.values,
                           data_removed=df_removed.values,
                           data_matched=df_matched.values,
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
        status = request.form['status']
        if('idx' in request.form):
            patient.update_rec_status(idx=int(request.form['idx']), status=status)
            if(status == 'M'):
                patient.update_rec_status(status=status)
        else:
            patient.update_rec_status(status=status)

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
        patient.update_rec_status(idx=idx, status="W")
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
