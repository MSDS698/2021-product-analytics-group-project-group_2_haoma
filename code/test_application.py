"""
Testing script for our application.
"""
from app.funcs import get_hh_agencies
import numpy as np
from app.classes import HHCare_Zipcodes


def test_zipcode_matches():
    """
    Ensure that the zipcode function gets the correct
    list of Home Health agencies.
    """

    assert all(get_hh_agencies('36609')['Provider Name'] ==
               np.array(['AMEDISYS HOME HEALTH CARE',
                         'SAAD HEALTHCARE',
                         'COMFORT CARE COASTAL HOME HEALTH',
                         'INFIRMARY HOMECARE',
                         'SPRINGHILL HOME HEALTH AND HOSPICE',
                         'AMEDISYS HOME HEALTH OF FOLEY',
                         'ENCOMPASS HEALTH HOME HEALTH',
                         'KINDRED AT HOME',
                         'PROHEALTH-GULF COAST, LLC']))

    assert all(get_hh_agencies('92543')['Provider Name'] ==
               np.array(['VNA CALIFORNIA',
                         'LOMA LINDA UNIV MED CTR HHA',
                         'ACCENTCARE HOME HEALTH OF CALIFORNIA, INC',
                         'NEW VISION HOME HEALTH AGENCY, INC',
                         'DSP HOME HEALTH INC',
                         'KAISER, RIVERSIDE, HOME HEALTH AGENCY (PARENT)',
                         'AGAPE HOME CARE',
                         'MISSION HOME HEALTH OF SAN DIEGO INC',
                         'IDEAL HOME CARE INC',
                         'CHARTER HEALTH CARE GROUP, LLC',
                         'JAMECO HOME HEALTH AGENCY INC', 'LORIAN HEALTH',
                         'VALLEY CARE HOME HEALTH SERVICES, INC',
                         'VISION HOME HEALTH AND HOSPICE CARE, INC',
                         'VANURA HOME HEALTH SERVICES, INC',
                         'VICTORY HOME HEALTH AGENCY',
                         'LEGACY HEALTH CARE PROVIDERS INC',
                         'HOME CARE EXCELLENCE HEALTH SERVICES, INC',
                         'INTERNATIONAL HOME HEALTH CARE, INC',
                         'N & D HEALTHCARE SERVICES INC',
                         'DESTINY HOME HEALTH AGENCY, INC',
                         'ST MARTIN HOME HEALTHCARE',
                         "A'S HOME HEALTH CARE, INC",
                         'COMPREHENSIVE HEALTH CARE, INC',
                         'HEMET HOME HEALTH CARE',
                         'FLOWER HOME HEALTH, INC',
                         'INLAND VALLEY HOME HEALTH AGENCY',
                         'WESCARE HOME HEALTH PROVIDERS INC',
                         'HOLY INFANT HOME CARE, INC',
                         'BRIDGE HOME HEALTH INLAND EMPIRE',
                         'AFFINITY HOME HEALTH CARE SERVICES, INC',
                         'BRIO HOME HEALTH SERVICES, INC',
                         'HEALTHNET HOME CARE SERVICES, INC',
                         'UNI CARE HOME HEALTH INC',
                         'SAN DIEGO HOME HEALTH CARE SERVICES INC',
                         'GRAPEVINE HOMECARE, INC',
                         'OPTIMA HOME HEALTH SERVICES',
                         'CAREWELL HOME HEALTH, INC',
                         'JM HOMECARE SOLUTIONS, INC',
                         'ALSA HOME HEALTH CARE, INC',
                         'SUNCREST HOME HEALTH SERVICES INC',
                         'HORIZON VALLEY HOME HEALTH CARE INC',
                         'DIRECT PROVIDER OF HEALTHCARE SERVICES, INC',
                         'LORIAN HEALTH',
                         'VIGILANS HOME HEALTH SERVICES, INC',
                         'KENO HOME HEALTH AGENCY LLC',
                         'ONORIA HEALTH CARE PROVIDER INC HOME HEALTH AND HO',
                         'CROWN HOME HEALTH CORPORATION',
                         'ADVANTAGE HEALTH SYSTEMS',
                         'EMERALD TRIUNE HOME HEALTH SERVICES, INC',
                         'ALL IN ONE HOME HEALTH AGENCY INC',
                         'ALTERNATIVE HEALTH CARE, LLC',
                         'ALLIANCE HOME HEALTH CARE SERVICES, INC.',
                         'CALIFORNIA HOME HEALTH AGENCY',
                         'VIP HEALTHCARE SERVICES LLC',
                         'HEALTHY LIVING AT HOME - PALM DESERT, LLC',
                         'PRISTINE CARE HOME HEALTH SERVICES, INC',
                         'ASPIRE HEALTHCARE SERVICES',
                         'PARAMOUNT HOME HEALTH CARE',
                         'ADVANCE SPECIALTY CARE SOUTH, INC.',
                         'DESCANSO HOME HEALTH SERVICES, INC',
                         'FIRST CHOICE HOME HEALTH AGENCY']))

    assert all(get_hh_agencies('99503')['Provider Name'] ==
               np.array(['PROVIDENCE IN HOME SERVICES',
                         'ANCORA HOME HEALTH & HOSPICE',
                         'FRONTIER HOME HEALTH',
                         'MAXIM HEALTHCARE SERVICES, INC',
                         'ALASKAN HOME HEALTH, INC',
                         'INFINITE CARE OF ALASKA',
                         'WELLSPRING HOME HEALTH CENTER']))

    assert all(get_hh_agencies('94118')['Provider Name'] ==
               np.array(['SUTTER VISITING NURSE ASSOCIATION AND HOSPICE',
                         'KAISER FOUNDATION HOSP HOME HEALTH - SAN FRANCISCO',
                         'PATHWAYS HOME HEALTH AND HOSPICE',
                         'ACCENTCARE HOME HEALTH OF CALIFORNIA, INC',
                         'SELF-HELP HOMECARE & HOSPICE',
                         'HEALTH AT HOME',
                         'AMEDISYS HOME HEALTH CARE',
                         'PROFESSIONAL HOME CARE ASSOCIATES',
                         'BAY AREA CARE TEAM INC',
                         'ASIAN NETWORK PACIFIC HOME CARE, INC',
                         'ASIAN AMERICAN HOME HEALTH',
                         'CROSSROADS HOME HEALTH & HOSPICE',
                         'INCARE HOME HEALTH SERVICES',
                         'NURSING & REHAB AT HOME',
                         'NEW HAVEN HOME HEALTH SERVICES, INC.',
                         'AMERICAN CAREQUEST',
                         'WARM SPRINGS HOME HEALTH, INC',
                         'HEALTH LINK HOME HEALTH AGENCY',
                         'ANX HOME HEALTHCARE',
                         'BLOSSOM RIDGE HEALTH, LLC',
                         'PREMIER HOME HEALTH PROVIDERS INC.',
                         'TRUEMED, INC',
                         'CARELINK HOME HEALTH AGENCY',
                         'HEALTHY LIVING AT HOME, INC.',
                         'AMITY HOME HEALTH CARE INC',
                         'FARALLON HOME HEALTH CARE, LLC',
                         'ST JUDE HOME HEALTH AGENCY',
                         'AMORE HOME HEALTH',
                         'HARMONY HOME HEALTH',
                         'HEALTHFLEX HOME HEALTH SERVICES',
                         'CARE IN TOUCH HOME HEALTH AGENCY',
                         'CVH CARE',
                         'BEST HOME HEALTH PROVIDERS, INC',
                         'ASSIST ON CALL PROFESSIONAL IN-HOME CARE SERVICES',
                         'SEHAJ HOME HEALTH, INC',
                         'ADVANCED HEALTHCARE SERVICES, LLC',
                         'ASTRA HEALTH CARE HOME HEALTH AGENCY',
                         '1ST CHOICE HOME HEALTH CARE', 'NEOGEN CARE',
                         '21ST CENTURY HOME HEALTH SERVICES INC.',
                         'HEALTH NOW HOME HEALTHCARE, INC',
                         'ELITE CARE HOME HEALTH AGENCY, INC.',
                         'HARMONY HOME HEALTH',
                         'CALIFORNIA HOME HEALTH L.L.C.',
                         'ALLIANCE HOME HEALTH',
                         'SOUTH BAY HOME HEALTH CARE, LLC',
                         'HOME HEALTH BAY AREA INC.']))

def test_database_connection():
     "Test the connection to our RDS database."
     record = HHCare_Zipcodes.query.get((27001, 99501)).state
     assert record == 'AK'


