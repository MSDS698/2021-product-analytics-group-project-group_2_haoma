import numpy as np
import pandas as pd
from   sklearn.pipeline              import *
from   sklearn.preprocessing         import *
import spacy



class Drop():
    """Drop Unnecessary Columns"""
    def __init__(self):
        ...
    def transform(self, X): 
        drop_cols = ['State', 'DTC Numerator', 'Type of Ownership',
                    'Quality of patient care star rating',
                    'DTC Denominator','DTC Risk-Standardized Rate',
                    'DTC Performance Categorization',
                    'DTC Risk-Standardized Rate (Lower Limit)',
                    'DTC Risk-Standardized Rate (Upper Limit)', 
                    'PPR Performance Categorization',
                    'PPR Numerator', 'PPR Denominator',
                    'PPR Risk-Standardized Rate',
                    'PPR Risk-Standardized Rate (Lower Limit)',
                    'PPR Risk-Standardized Rate (Upper Limit)',
                    'How much Medicare spends on an episode of care at this agency, '+\
                    'compared to Medicare spending across all agencies nationally',
                    'No. of episodes to calc how much Medicare spends per episode of '+\
                    'care at agency, compared to spending at all agencies (national)']
        X = X.drop(columns = drop_cols)
        return X

    def fit(self, X, y=None):
        return self
    
class Rename():
    """Rename Columns"""
    def __init__(self):
        ...
        
    def transform(self, X): 
        X.columns = ['ccn', 'name', 'address', 'city',' zip', 'phone', 'nursing', 'pt', 'ot', 'speech', 'social', 'aide', 'date',
                 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16',
                 'Q17', 'dtc', 'ppr']
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
        X = X.drop(columns = services)
        return X

    def fit(self, X, y=None, **fit_params):
        return self
    
class Recommend():
    """Input: list of boolean values pertaining to offered services
       Output: filtered df of agencies based on offered services"""
    def __init__(self, 
                 tier_weights,
                 flagged_qtopic,
                 num_agencies):
        self.tier_weights = tier_weights
        self.flagged_qtopic = flagged_qtopic
        self.num_agencies = num_agencies
        self.star_cols = ['Q1', 'Q13', 'Q8', 'Q9', 'Q10', 'Q11', 'Q15']  
        self.Q_dict = {'Q3':'falling', 
                       'Q4':'depression', 
                       'Q5':'flu', 
                       'Q6': 'pneumonia', 
                       'Q7': 'diabetes', 
                       'Q8': 'moving', 
                       'Q9': 'getting_in_bed',
                       'Q10': 'bathing', 
                       'Q11':'breathing', 
                       'Q12': 'wounds', 
                       'Q16': 'skin_integrity'}

    def transform(self, X, **transform_params): 
        q_columns = X.columns[7:]

        # initialize weights
        weight = {key:1 for key in q_columns}
        filtered_qs = [key for key, value in self.flagged_qtopic.items() if value]  

        for col in self.star_cols:
            weight[col] += self.tier_weights['star']

        for col in filtered_qs:
            weight[col] += self.tier_weights['flagged']

        weight['ppr'] = self.tier_weights['ppr']
        weight['dtc'] = self.tier_weights['dtc']

        # apply weights
        for col in X:
            if col in weight.keys():
                X[col] = X[col] * weight[col]

        # sort recommendations
        X['score'] = X[q_columns].sum(axis=1)
        X = X.sort_values('score', ascending=False).iloc[:self.num_agencies]
                
        renamed_cols = [self.Q_dict[col] for col in filtered_qs]
        rename_dict = dict(zip(filtered_qs, renamed_cols))
        
        X = X.rename(columns=rename_dict)
        return_cols = ['name', 'ppr', 'dtc'] + renamed_cols + ['score']
        
        df_rec = X[return_cols]
        
        denominator = 3
        df_rec[renamed_cols] = round(df_rec[renamed_cols]/denominator,2)
        df_rec['score'] = round((df_rec.score/df_rec.score.max())*100, 2)
        df_rec['ppr'] = round(df_rec.ppr/2,2)

        return X, df_rec

    def fit(self, X, y=None, **fit_params):
        return self
    

    
class custom_imputer():
    """
    Imputs Q columns with worst value
    Assumes that questions with good answers being a higher value will be, 
    on average, higher than 50% (0.5)
    """
    def __init__(self):
        ...
    def transform(self, X): 
        q_columns = X.columns[8:]

        col_values = X[q_columns]
        high_is_better = False
        if np.nanmean(col_values) > 50:
            high_is_better = True
        if not high_is_better:
            col_values = np.ones_like(col_values)*100 - col_values
        df_impute = col_values.fillna(np.nanmin(col_values))
        return X.iloc[:,:8].join(df_impute)

    def fit(self, X, y=None, **fit_params):
        return self

    
class change_ascending_cols():
    """
    Transforms the ascending columns to
    descending to prepare for the recommendation sum
    """
    def __init__(self):
        self.max_cols = ['ppr', 'Q14', 'Q15', 'Q16']
        
    def transform(self, X): 
        for col in self.max_cols:
            X[col] = round((100-X[col]), 2)
        return X

    def fit(self, X, y=None, **fit_params):
        return self


    
    


def renamed_qcols(df):
    """Renamed Qualitative Columns"""
    long_questions = df.columns[16:33]
    short_questions = [f'Q{i+1}' for i in range(17)]

    new_columns = []
    for i,col in enumerate(df.columns):
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
    cms_nums = df_zip[df_zip[' ZIP Code'] == zipcode]['CMS Certification Number (CCN)']
    df_cal = df_cal[df_cal['CMS Certification Number (CCN)'].isin(list(cms_nums))]
    return df_cal