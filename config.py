import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'opms'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/opms'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPGRADE_PER_PAGE = 3