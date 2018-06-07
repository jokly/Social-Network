import os
from os.path import join, dirname, realpath

class Config(object):
    IS_DEV = os.environ.get('IS_PRODUCTION') is None
    SECRET_KEY = 'test-secret-key'
    POSTGRES_URL = '127.0.0.1:5432'
    POSTGRES_USER = 'postgres'
    POSTGRES_PW = 'root'
    POSTGRES_DB = 'social_network'
    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
            user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = 'static'
    AVATARS_FOLDER = join(dirname(realpath(__file__)), 'app', STATIC_FOLDER, 'avatars')
    POSTS_IMG_FOLDER = join(dirname(realpath(__file__)), 'app', STATIC_FOLDER, 'posts_img')
