import numpy as np
import pandas as pd
from sklearn.pipeline import *
from sklearn.preprocessing import *
import spacy


class Drop():
    """Drop Unnecessary Columns"""
    def __init__(self):
        ...

    def transform(self, X):
        drop_cols = ['State', 'DTC Numerator', 'Type of Ownership',
                     'DTC Denominator', 'DTC Risk-Standardized Rate',
                     'DTC Risk-Standardized Rate (Lower Limit)',
                     'DTC Risk-Standardized Rate (Upper Limit)',
                     'PPR Numerator', 'PPR Denominator',
                     'PPR Risk-Standardized Rate',
                     'PPR Risk-Standardized Rate (Lower Limit)',
                     'PPR Risk-Standardized Rate (Upper Limit)',
                     'How much Medicare spends on an episode of care at ' +
                     'this agency, compared to Medicare spending across ' +
                     'all agencies nationally',
                     'No. of episodes to calc how much Medicare spends ' +
                     'per episode of care at agency, compared to spending ' +
                     'at all agencies (national)']
        X = X.drop(columns=drop_cols)
        return X

    def fit(self, X, y=None):
        return self


class Rename():
    """Rename Columns"""
    def __init__(self):
        ...

    def transform(self, X):
        X.columns = ['ccn', 'name', 'address', 'city', ' zip',
                     'phone', 'nursing', 'pt', 'ot', 'speech',
                     'social', 'aide', 'date', 'star', 'Q1',
                     'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8',
                     'Q9', 'Q10', 'Q11', 'Q12', 'Q13', 'Q14',
                     'Q15', 'Q16', 'Q17', 'dtc', 'dtc_cat', 'ppr',
                     'ppr_cat']
        return X

    def fit(self, X, y=None, **fit_params):
        return self


class FilterByService():
    """Input: list of boolean values pertaining to offered services
       Output: filtered df of agencies based on offered services"""
    def __init__(self, bool_services):
        self.bool_services = bool_services

    def transform(self, X, **transform_params):
        services = ['nursing', 'pt', 'ot', 'speech', 'social', 'aide']
        services_dict = dict(zip(services, self.bool_services))
        for service in services:
            if services_dict[service]:
                X = X[X[service] == 'Yes']
        X = X.drop(columns=services)
        return X

    def fit(self, X, y=None, **fit_params):
        return self


class Recommend():
    """Input: list of boolean values pertaining to offered services
       Output: filtered df of agencies based on offered services"""
    def __init__(self, Q_flagged, num_agencies):
        self.Q_flagged = Q_flagged
        self.num_agencies = num_agencies

    def transform(self, X, **transform_params):
        sort_cols = self.Q_flagged + ['star']
        X = X.sort_values(by=sort_cols, ascending=False)
        return X.iloc[:self.num_agencies]

    def fit(self, X, y=None, **fit_params):
        return self


def text_process(s):
    """Text-Preprocessing"""
    nlp = spacy.load('en_core_web_sm')
    string = nlp(s)
    filtered_list = []
    for token in string:
        if token.is_stop or len(token) < 3:
            continue
        filtered_list.append(token.text.lower())
    return filtered_list


def renamed_qcols(df):
    """Renamed Qualitative Columns"""
    long_questions = df.columns[16:33]
    short_questions = [f'Q{i+1}' for i in range(17)]

    new_columns = []
    for i, col in enumerate(df.columns):
        if col not in long_questions:
            new_columns.append(col)
        else:
            new_columns.append(short_questions[i-16])
    df.columns = new_columns
    return df


def load_df(zipcode):
    df = pd.read_csv('data/HH_Provider_Oct2020.csv')
    df_cal = df[df['State'] == 'CA']
    df_cal.reset_index(drop=True, inplace=True)
    df_cal = df_cal.loc[:, ~df_cal.columns.str.startswith('Footnote')]
    df_zip = pd.read_csv('data/HH_Zip_Oct2020.csv')
    cms_nums = df_zip[df_zip[' ZIP Code']
                      == zipcode]['CMS Certification Number (CCN)']
    df_cal = df_cal[df_cal['CMS Certification Number (CCN)']
                    .isin(list(cms_nums))]
    return df_cal
