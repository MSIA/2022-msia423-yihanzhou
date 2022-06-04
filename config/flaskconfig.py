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

# Categorical questions used in the app
MODEL_TYPE = ['5 Series', '6 Series', '1 Series', '7 Series', '2 Series',
              '4 Series', 'X3', '3 Series', 'X5', 'X4', 'i3', 'X1', 'M4', 'X2',
              'X6', '8 Series', 'Z4', 'X7', 'M5', 'i8', 'M2', 'M3', 'M6', 'Z3']
TRANSMISSION_TYPE = ['Automatic', 'Manual', 'Semi-Auto']
FUELTYPE = ['Diesel', 'Petrol', 'Other', 'Hybrid', 'Electric']
ENGINESIZE = [2.0, 3.0, 1.5, 0.6, 1.6, 4.4, 0.0, 2.2, 2.5, 4.0, 3.2, 1.0, 5.0,
              1.9, 6.6, 2.8, 3.5]
