agency_df_keys = {
    'daily_activities': [
        'name',
        'better_bathing',
        'better_getting_in_bed',
        'better_moving'
    ],
    'treating_symptoms': ['name',
                          'improve_breathing',
                          'improve_wounds',
                          'changed_skin'],
    'preventing_harm': ['checked_falling',
                        'checked_depression',
                        'checked_flu',
                        'checked_pneumonia'],
    'falling': 'checked_falling',
    'depression': 'checked_depression',
    'flu': 'checked_flu',
    'pneumonia': 'checked_pneumonia',
    'taught_med': 'taught_meds',
    'timely_med': 'timely_address_meds',
    'diabetes': 'diabetes_foot',
    'timely': 'timely_manner',
    'dtc': 'discharge_community',
    'er': 'ER',
    'readmitted': 'readmitted',
}

dashboard_info = {
    'daily': {
        'title': 'Managing Daily Activities',
        'body': """
            <h8 class="card-text">How often the patient got better at :</h8>
            <ul>
                <li>Bathing</li>
                <li>Getting In and Out of the Bed</li>
                <li>Walking or Moving Around</li>
            </ul>""",
        'height_desc': '15rem',
        'height_data': '13rem',
    },
    'symptom': {
        'title': 'Treating Symptoms',
        'body': """
            <ul>
                <li>How often breathing improved</li>
                <li>How often wounds improved</li>
                <li>How often pressure ulcers didn't worsen</li>
            </ul>""",
        'height_desc': '15rem',
        'height_data': '13rem',
    },
    'timely': {
        'title': 'Timely Manner',
        'body': """
            <p class="card-text">
                How often did the agency begin their patients' care in a timely manner?
            </p>""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'ppr': {
        'title': 'Preventable Readmission',
        'body': """
            <p class="card-text">
                The risk-standardized rate of unplanned, potentially preventable readmissions for
                patients within 30 days of discharge.
            </p>""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'dtc': {
        'title': 'Discharge to Community',
        'body': """
            <p class="card-text">
                Percent of patients who were discharged to the community within 100 
                days of the start of the episode, and remained in the community for 30 
                consecutive days 
            </p>""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'er': {
        'title': 'ER Visits',
        'body': """
            <p class="card-text">
                How often patients receiving home health care needed any urgent, 
                unplanned care in the hospital emergency room – without being 
                admitted to the hospital
            </p>""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'readmitted': {
        'title': 'Readmitted',
        'body': """
            <p class="card-text">
                How often home health patients did not have to be admitted to the hospital
            </p>""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'falling': {
        'title': 'Risk of Falling',
        'body': """
            <p class="card-text">
                How often the home health team checked patients' risk of falling?
            </p>""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'depression': {
        'title': 'Depression',
        'body': """
            <p class="card-text">
                How often the home health team checked patients for depression?
            </p>""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'pneumonia': {
        'title': 'Pneumococcal Vaccine',
        'body': """
            <p class="card-text">
                How often the home health team made sure that their patients have received a pneumococcal vaccine (pneumonia shot)
            </p>""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'flu': {
        'title': 'Flu Shot',
        'body': """
            <p class="card-text">
                How often the home health team determined whether patients received a flu shot for the current flu season
            </p>""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'timely_med': {
        'title': 'Medication',
        'body': """
            <p class="card-text">
                How often patients got better at taking their drugs correctly by mouth
            </p>""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'taught_med': {
        'title': 'Taught Meds',
        'body': """
            <p class="card-text">
                How often the home health team taught patients (or their family caregivers) about their drugs
            </p>""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'diabetes': {
        'title': 'Diabetes and Foot Care',
        'body': """
            <p class="card-text">
                For patients with diabetes, how often the home health team got doctor's orders, gave foot care, and taught patients about foot care
            </p>""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
}

dashboard_chart_titles = {k:dashboard_info[k]['title'] for k in dashboard_info}

dashboard_key_order = [
    'daily',
    'symptom',
    'timely',
    'ppr',
    'dtc',
    'er',
    'readmitted',
    'falling',
    'depression',
    'pneumonia',
    'flu',
    'timely_med',
    'taught_med',
    'diabetes'
]

dashboard_chart_types = {
    'daily': 'bar',
    'symptom': 'bar',
    'timely': 'doughnut',
    'ppr': 'doughnut',
    'dtc': 'doughnut',
    'er': 'doughnut',
    'readmitted': 'doughnut',
    'falling': 'doughnut',
    'depression': 'doughnut',
    'pneumonia': 'doughnut',
    'flu': 'doughnut',
    'timely_med': 'doughnut',
    'taught_med': 'doughnut',
    'diabetes': 'doughnut',
}

dashboard_barchart_labels = {
    'daily': ['Bath', 'Bed', 'Move'],
    'symptom': ['Breathing', 'Wounds', 'Skin'],
}

dashboard_colors = ['#cc3d33', '#dea004', '#3378cc']
background_colors = ['rgba(204, 61, 51, 0.8)', 'rgba(222, 160, 4, 0.8)', 'rgba(51, 120, 204, 0.8)']