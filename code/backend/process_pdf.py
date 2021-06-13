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

pages = convert_from_path(pdf_path)

im_count = 0
for page in pages:
    fname = f'page_{str(im_count)}.jpg'
    page.save(f'images/{fname}', 'JPEG')
    im_count += 1

filelimit = im_count-1

output = 'output.txt'
with open(output, 'a') as f:
    for i in range(0, filelimit):
        fname = f'images/page_{str(i)}.jpg'
        image = Image.open(fname)
        text = str(((pytesseract.image_to_string(image))))
        text = text.replace('-\n', '')    
        f.write(text)

output = 'output.txt'
with open(output, 'r')  as f:
    text = f.read()

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