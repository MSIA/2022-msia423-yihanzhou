import os
DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 5000
APP_NAME = "bmw_price_estimator"
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

DB_HOST = os.environ.get('MYSQL_HOST')
DB_PORT = os.environ.get('MYSQL_PORT')
DB_USER = os.environ.get('MYSQL_USER')
DB_PW = os.environ.get('MYSQL_PASSWORD')
DATABASE = os.environ.get('DATABASE_NAME')
DB_DIALECT = 'mysql+pymysql'
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
if SQLALCHEMY_DATABASE_URI is not None:
    pass
elif DB_HOST is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/msia423_db.db'
else:
    SQLALCHEMY_DATABASE_URI = f'{DB_DIALECT}://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DATABASE}'

