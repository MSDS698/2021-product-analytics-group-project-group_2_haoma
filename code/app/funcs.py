"""
Script containing all necessary functions
for our application. These are kept
separate from routes to improve
readability and help with debugging.
"""
import pandas as pd

# Contains xipcodes that HH agencies cover
HH_ZIP_DATA_URL = "https://data.cms.gov/provider-data/sites/default/files/" \
                  "resources/35759790ad0a207f47ba2a079eb51a0f_1620794404/" \
                  "HH_Zip_Oct2020.csv"

# Contains information on HH agencies
HH_DATA_URL = "https://data.cms.gov/provider-data/sites/default/files/" \
              "resources/1ee6a6e80907bf13661aa2f099415fcd_1620794404/" \
              "HH_Provider_Oct2020.csv"


def get_hh_agencies(zipcode: str):
    "Get a df of Home Health agencies that cover a given zipcode."

    df_zip = pd.read_csv(HH_ZIP_DATA_URL)
    df_data = pd.read_csv(HH_DATA_URL)
    cms_nums = df_zip[df_zip[' ZIP Code'] ==
                      int(zipcode)]['CMS Certification Number (CCN)']
    hh_data = df_data[df_data['CMS Certification Number (CCN)']
                      .isin(cms_nums)][['Provider Name',
                                        'Address',
                                        'City',
                                        'Phone']]
    return hh_data
