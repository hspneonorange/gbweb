import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://gbweb:Baby1c@t@127.0.0.1/gbweb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
