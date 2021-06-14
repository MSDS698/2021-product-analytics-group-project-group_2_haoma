"""
Script containing all necessary functions
for our application. These are kept
separate from routes to improve
readability and help with debugging.
"""
import pandas as pd
from urllib.parse import urlencode
from app.classes import HHCare_Zipcodes
from config import GEOCODE_ENDPOINT
from app import s3
import requests
import re
import os


def get_hh_agencies(zipcode: str):
    "Get a df of Home Health agencies that cover a given zipcode."
    response = s3.get_object(Bucket="haoma-bucket", Key="HH_Zip_Oct2020.csv")
    df_zip = pd.read_csv(response.get("Body"))
    response = s3.get_object(Bucket="haoma-bucket",
                             Key="HH_Provider_Oct2020.csv")
    df_data = pd.read_csv(response.get("Body"))
    cms_nums = df_zip[df_zip[' ZIP Code'] ==
                      int(zipcode)]['CMS Certification Number (CCN)']
    hh_data = df_data[df_data['CMS Certification Number (CCN)']
                      .isin(cms_nums)][['Provider Name',
                                        'Address',
                                        'City',
                                        'Phone']]
    return hh_data


def get_hh_agencies_rds(zipcode: str):
    "Same as get_hh_agencies but with the RDS rather than S3."
    cms_nums = HHCare_Zipcodes.query.with_entities(HHCare_Zipcodes.
                                                   cms_certification_number) \
        .filter_by(zip_code=zipcode).all()

    # cms_nums is list of tuples, want list of values
    cms_nums = [tup[0] for tup in cms_nums]
    response = s3.get_object(Bucket="haoma-bucket",
                             Key="HH_Provider_Oct2020.csv")
    df_data = pd.read_csv(response.get("Body"))
    hh_data = df_data[df_data['CMS Certification Number (CCN)']
                      .isin(cms_nums)][['Provider Name',
                                        'Address',
                                        'City',
                                        'Phone']]

    return hh_data


def geocode_address(address: str) -> dict:
    "Return a dict of lon, lat coordinates for a given address."
    params = {
        'address': address, 'key': os.getenv('HAOMA_GCP_API_KEY')
    }

    url = GEOCODE_ENDPOINT + urlencode(params)
    res = requests.get(url)
    res_dict = res.json()
    lat_lon = res_dict['results'][0]['geometry']['location']

    return lat_lon


def extract_patient_info(instance_path, filename, file) -> dict:
    file.save(os.path.join(
        instance_path, filename
    ))
    extracted_info = {}
    extracted_info['insurance'] = "insurance example type"
    extracted_info['summary'] = "summary example"
    return extracted_info

# get_hh_agencies()