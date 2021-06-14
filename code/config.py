import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:" \
        "gLnDyBz4EWsws5m@haoma-db.c2ifgz0co6no.us-west-2.rds" \
        ".amazonaws.com:5432/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.urandom(24)


GEOCODE_ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json?"
