"""
This file defines some functionality in the app
"""
import logging.config
import sqlite3
import traceback

import yaml
import sqlalchemy.exc
from flask import Flask, render_template, request

# For setting up the Flask-SQLAlchemy database session
from src.bmw_db import CarManager
from config.flaskconfig import MODEL_TYPE, TRANSMISSION_TYPE, FUELTYPE, ENGINESIZE
import src.predict as predict

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates",
            static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug(
    'Web app should be viewable at %s:%s if docker run command maps local '
    'port to the same port as configured for the Docker container '
    'in config/flaskconfig.py (e.g. `-p 5000:5000`). Otherwise, go to the '
    'port defined on the left side of the port mapping '
    '(`i.e. -p THISPORT:5000`). If you are running from a Windows machine, '
    'go to 127.0.0.1 instead of 0.0.0.0.', app.config["HOST"]
    , app.config["PORT"])

# Initialize the database session
car_manager = CarManager(app)

# Load yaml configuration file
# load yaml configuration file
try:
    with open('config/config.yaml', "r") as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)
        logger.info("Configuration file loaded")
except FileNotFoundError:
    logger.error("Configuration file is not found")


@app.route('/')
def index():
    """Main view that car information in the database.

    Create view into index page that uses data queried from BMW database and
    inserts it into the app/templates/index.html template.

    Returns:
         rendered html template located at: app/templates/index.html

    """

    # try:
    #     car_info = car_manager.session.query(Car).limit(
    #         app.config["MAX_ROWS_SHOW"]).all()
    #     logger.debug("Index page accessed")
    #     return render_template('index.html', car_info=car_info)

    try:
        logger.info("Index page accessed")
        return render_template('index.html',
                               model=MODEL_TYPE,
                               # year=year,
                               tranmission=TRANSMISSION_TYPE,
                               # mileage=mileage,
                               fuelType=FUELTYPE,
                               # mpg=mpg,
                               engineSize=ENGINESIZE
                               )
    except sqlite3.OperationalError as e:
        logger.error(
            "Error page returned. Not able to query local sqlite database: %s."
            " Error: %s ",
            app.config['SQLALCHEMY_DATABASE_URI'], e)
        return render_template('error.html')
    except sqlalchemy.exc.OperationalError as e:
        logger.error(
            "Error page returned. Not able to query MySQL database: %s. "
            "Error: %s ",
            app.config['SQLALCHEMY_DATABASE_URI'], e)
        return render_template('error.html')
    except:
        traceback.print_exc()
        logger.warning("Not able to display car information, error page returned")
        return render_template('error.html')


@app.route('/result', methods=['POST', 'GET'])
def add_entry():
    """View that process a POST with new car input

    Add new car information to database and get prediction results

    Returns:
        rendered html template located at: app/templates/result.html if successfully processed,
        rendered html template located at: app/templates/error.html if any error occurs
    """
    if request.method == 'GET':
        return "Visit the homepage to add applicants and get predictions"
    elif request.method == 'POST':
        try:
            car_manager.add_info(model=request.form['model'],
                                 year=request.form['year'],
                                 transmission=request.form['transmission'],
                                 mileage=request.form['mileage'],
                                 fuelType=request.form['fueltype'],
                                 mpg=request.form['mpg'],
                                 engineSize=request.form['enginesize'])
            logger.info("New car info added: %s by %s", request.form['model'],
                        request.form['year'])

            #Get the car price estimation on the new car information
            user_input = {'model': request.form['model'],
                          'year': request.form['year'],
                          'transmission': request.form['transmission'],
                          'mileage': request.form['mileage'],
                          'fuelType': request.form['fueltype'],
                          'mpg': request.form['mpg'],
                          'engineSize': request.form['enginesize']}
            user_input_transformed = predict.transform_input(user_input, **conf['predict']['transform_input'])
            ypred = predict.get_prediction(user_input_transformed, **conf['predict']['get_prediction'])[0]
            logger.info("The new car estimated price is generated")
            logger.debug("Result page accessed")
            return render_template('result.html', output=ypred)
        except:
            logger.warning("Not able to process your request, error page returned")
            return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"],
            host=app.config["HOST"])
