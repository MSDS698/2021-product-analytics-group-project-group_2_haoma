FROM python:3.8-buster
RUN apt update
RUN apt install git
RUN apt install -y tesseract-ocr

RUN git clone https://github.com/MSDS698/2021-product-analytics-group-project-group_2_haoma.git /2021-product-analytics-group-project-group_2_haoma
WORKDIR /2021-product-analytics-group-project-group_2_haoma

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

ENV FLASK_APP=code/app.py
ENV PYTHON_ENV=prod
CMD flask run --host=0.0.0.0 --port=80

EXPOSE 80