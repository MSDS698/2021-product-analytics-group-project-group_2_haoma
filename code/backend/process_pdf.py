import os
import sys
import string

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import spacy
import re


pdf_path = 'referral_example.pdf'


def get_text_from_pdf(path):
    with open(pdf_path, 'rb') as f:
        file = f.read()
    pages = convert_from_path(pdf_path, fmt='jpeg')
    text = ''.join(map(lambda x: pytesseract
                       .image_to_string(x).replace('-\n', ''), pages))
    return text


text = get_text_from_pdf(pdf_path)

# Initalize ordinal translations
translation_ws = {ord(c): ' ' for c in string.whitespace}
translation_punc = {ord(c): '' for c in string.punctuation}

# Translate/ clean text
text = text.translate(translation_ws)
text = text.translate(translation_punc)
text = ' '.join(text.split())
# pattern = re.compile(r'.*(9\d{4})')
# print(f'zipcode: {re.findall(pattern, text)}')
# zipcode = re.findall(pattern, text)


# Remove other Digits
translation_dig = {ord(c): '' for c in string.digits}
text = text.translate(translation_dig)
