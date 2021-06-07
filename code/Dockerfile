FROM python:3.8-buster
RUN apt install git

RUN git clone https://github.com/MSDS698/2021-product-analytics-group-project-group_2_haoma.git /2021-product-analytics-group-project-group_2_haoma
WORKDIR /2021-product-analytics-group-project-group_2_haoma

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP=code/app.py
CMD flask run --host=0.0.0.0 --port=80

EXPOSE 80