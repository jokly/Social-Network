import os

class Config(object):
    SECRET_KEY = 'test-secret-key'
    POSTGRES_URL = '127.0.0.1:5432'
    POSTGRES_USER = 'postgres'
    POSTGRES_PW = 'root'
    POSTGRES_DB = 'social_network'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
