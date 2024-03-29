import os
import sys
import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import re
import en_core_web_sm
from app.pipeline import *


def get_text_from_pdf(path):
    with open(path, 'rb') as f:
        file = f.read()
    pages = convert_from_path(path, fmt='jpeg')
    text = ''.join(map(lambda x: pytesseract
                       .image_to_string(x).replace('-\n', ''), pages))
    return text


def return_flagged(pdf_path, df_cal):
    text = return_text(pdf_path)
    word_list = text_process(text)
    df_cal = renamed_qcols(df_cal)

    # Create keyword lists
    q3_keys = ["falling", "fall", "fell", "tripped", "trip", "tumble"]
    q4_keys = ["depression", "mental", "bipolar",
               "sad", "upset", "trauma", "traumatic"]
    q5_keys = ["flu"]
    q6_keys = ["pneumonia", "pneumococcal"]
    q7_keys = ["diabetes", "foot"]
    q8_keys = ["walk", "walking", "moving"]
    q9_keys = ["bed"]
    q10_keys = ["bathing", "bathe", "bath"]
    q11_keys = ["breath", "shortness of breath",
                "shortness", "breathing", "breathe", "oxygen"]
    q12_keys = ["wound", "wounds", "cut", "slice", "lesion",
                "gash", "puncture", "slash", "laceration", "tear",
                "rent", "puncture", "slash", "sore", "graze", "scratch",
                "scrape", "abrasion", "bruise", "contusion", "trauma"]
    q16_keys = ["ulcer", "pressure", "skin", "swelling", "post-acute"]

    q_keys = [q3_keys, q4_keys, q5_keys, q6_keys, q7_keys, q8_keys,
              q9_keys, q10_keys, q11_keys, q12_keys, q16_keys]

    keys = [f'Q{i}' for i in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16]]
    flags = [any(set(x).intersection(set(word_list))) for x in q_keys]
    flagged_qtopic = dict(zip(keys, flags))
    return flagged_qtopic


def return_text(pdf_path):
    text = get_text_from_pdf(pdf_path)

    # Initalize ordinal translations
    translation_ws = {ord(c): ' ' for c in string.whitespace}
    translation_punc = {ord(c): '' for c in string.punctuation}

    # Translate/ clean text
    text = text.translate(translation_ws)
    text = text.translate(translation_punc)
    text = ' '.join(text.split())

    # Remove other Digits
    translation_dig = {ord(c): '' for c in string.digits}
    text = text.translate(translation_dig)
    return text


def text_process(s):
    """Text-Preprocessing"""
    nlp = en_core_web_sm.load()
    string = nlp(s)
    filtered_list = []
    for token in string:
        if token.is_stop or len(token) < 3:
            continue
        filtered_list.append(token.text.lower())
    return filtered_list
