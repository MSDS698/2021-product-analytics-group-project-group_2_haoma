import pandas as pd
from app import s3
from app.preprocess import *


class Recommender():
    score_keys = ['score_1_name', 'score_2_name', 'score_3_name']

    def __init__(self):
        # Pull data once
        response = s3.get_object(Bucket="haoma-bucket",
                                 Key="HH_Provider_Oct2020.csv")
        df = pd.read_csv(response.get("Body"))
        df_cal = df[df['State'] == 'CA']
        df_cal.reset_index(drop=True, inplace=True)
        self.df_cal = df_cal.loc[:, ~df_cal.columns.str.startswith('Footnote')]
        response = s3.get_object(Bucket="haoma-bucket",
                                 Key="HH_Zip_Oct2020.csv")
        self.df_zip = pd.read_csv(response.get("Body"))
        # Hyperparameters
        self.tier_weights = {'star': 0, 'flagged': 2,
                             'ppr': 2, 'dtc': 1}
        self.num_agencies = 10

    def filter_zipcode(self, zipcode):
        cms_nums = self.df_zip[self.df_zip[' ZIP Code']
                               == zipcode]['CMS Certification Number (CCN)']
        df_filter = self.df_cal[self
                                .df_cal['CMS Certification Number (CCN)']
                                .isin(list(cms_nums))]
        return df_filter

    def recommend(self, df_filter, bool_services, pdf_path):
        # Go through pipeline
        flagged_qtopic = return_flagged(pdf_path, df_filter)
        pipe_prep = Pipeline([('Drop Unnecessary Columns', Drop()),
                              ('Rename Columns', Rename()),
                              ('Filter Offered Services',
                               FilterByService(bool_services)),
                              ('Impute Values', custom_imputer()),
                              ('Normalize/Reverse Asc. Columns',
                               change_ascending_cols()),
                              ('Recommend', Recommend(self.tier_weights,
                                                      flagged_qtopic,
                                                      self.num_agencies))])
        df, df_rec = pipe_prep.fit_transform(df_filter.copy())
        return df['name'].tolist()

    def get_metrics(self, recommendations, summary):
        ...
        scores = {}
        for agency in recommendations:
            scores[agency] = {}
            scores[agency][self.score_keys[0]] = 10
            scores[agency][self.score_keys[1]] = 7
            scores[agency][self.score_keys[2]] = 8
        return scores

    def get_column_names(self):
        names = []
        for k in self.score_keys:
            names += [" ".join(k.split("_")).title()]
        return names
