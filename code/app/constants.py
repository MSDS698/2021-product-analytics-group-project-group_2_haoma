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
            How often the patient got better at :
            <div>
                <ul>
                    <li>Bathing</li>
                    <li>Getting In and Out of the Bed</li>
                    <li>Walking or Moving Around</li>
                </ul>
            </div>""",
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
        'body': """How often did the agency begin their patients' care in a timely manner?""",
        'height_desc': '19rem',
        'height_data': '100%',
    },
    'ppr': {
        'title': 'Preventable Readmission',
        'body': """The risk-standardized rate of unplanned, potentially preventable readmissions for
                patients within 30 days of discharge.""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'dtc': {
        'title': 'Discharge to Community',
        'body': """Percent of patients who were discharged to the community within 100 
                days of the start of the episode, and remained in the community for 30 
                consecutive days""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'er': {
        'title': 'ER Visits',
        'body': """How often patients receiving home health care needed any urgent, 
                unplanned care in the hospital emergency room – without being 
                admitted to the hospital""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'readmitted': {
        'title': 'Readmitted',
        'body': """How often home health patients did not have to be admitted to the hospital""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'falling': {
        'title': 'Risk of Falling',
        'body': """How often the home health team checked patients' risk of falling?""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'depression': {
        'title': 'Depression',
        'body': """How often the home health team checked patients for depression?""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'pneumonia': {
        'title': 'Pneumococcal Vaccine',
        'body': """How often the home health team made sure that their patients have received a pneumococcal vaccine (pneumonia shot)""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'flu': {
        'title': 'Flu Shot',
        'body': """How often the home health team determined whether patients received a flu shot for the current flu season""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'timely_med': {
        'title': 'Medication',
        'body': """How often patients got better at taking their drugs correctly by mouth""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'taught_med': {
        'title': 'Taught Meds',
        'body': """How often the home health team taught patients (or their family caregivers) about their drugs""",
        'height_desc': '19rem',
        'height_data': '17rem',
    },
    'diabetes': {
        'title': 'Diabetes and Foot Care',
        'body': """For patients with diabetes, how often the home health team got doctor's orders, gave foot care, and taught patients about foot care""",
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

dashboard_colors = ['#cc3d33', '#dea004', '#3378cc', '#b30098', '#7d4700']
background_colors = ['rgba(204, 61, 51, 0.8)', 'rgba(222, 160, 4, 0.8)', 'rgba(51, 120, 204, 0.8)', '#b30098', '#7d4700']