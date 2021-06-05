"""
Testing script for our application.
"""
from app.funcs import get_hh_agencies
import numpy as np

def test_zipcode_matches():
	"Ensure that the zipcode function gets the correct list of Home Health agencies."
	assert all(get_hh_agencies('36609')['Provider Name'] == np.array([
		'AMEDISYS HOME HEALTH CARE','SAAD HEALTHCARE','INFIRMARY HOMECARE',
		'ENCOMPASS HEALTH HOME HEALTH','KINDRED AT HOME'
	]))
	assert all(get_hh_agencies('92543')['Provider Name'] == np.array(['HEMET HOME HEALTH CARE']))
	assert all(get_hh_agencies('99503')['Provider Name'] == np.array(['FRONTIER HOME HEALTH',
                                                                      'MAXIM HEALTHCARE SERVICES, INC']))
	assert all(get_hh_agencies('94118')['Provider Name'] == np.array(['KAISER FOUNDATION HOSP HOME HEALTH - SAN FRANCISCO']))