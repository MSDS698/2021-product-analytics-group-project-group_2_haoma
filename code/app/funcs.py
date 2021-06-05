"""
Script containing all necessary functions
for our application. These are kept 
separate from routes to improve
readability and help with debugging.
"""
import pandas as pd

HH_DATA_URL = "https://data.cms.gov/provider-data/sites/default/files/resources/1ee6a6e80907bf13661aa2f099415fcd_1620794404/HH_Provider_Oct2020.csv"


def get_hh_agencies(zipcode: str):
	"Get a df of Home Health agencies from given zipcode."
	df = pd.read_csv(HH_DATA_URL)
	hh_data = df[df.ZIP == int(zipcode)][['Provider Name', 'Address', 'City', 'Phone']]
	return hh_data