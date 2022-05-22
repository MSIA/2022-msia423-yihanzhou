import logging.config
import sqlite3
import traceback

import sqlalchemy.exc
from flask import Flask, render_template, request, redirect, url_for

# For setting up the Flask-SQLAlchemy database session
from src.bmw_db import CarManager, Car

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


@app.route('/')
def index():
    """Main view that car information in the database.

    Create view into index page that uses data queried from BMW database and
    inserts it into the app/templates/index.html template.

    Returns:
        Rendered html template

    """

    try:
        car_info = car_manager.session.query(Car).limit(
            app.config["MAX_ROWS_SHOW"]).all()
        logger.debug("Index page accessed")
        return render_template('index.html', car_info=car_info)
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
        logger.error("Not able to display car infomation, error page returned")
        return render_template('error.html')


@app.route('/result', methods=['POST'])
def add_entry():
    """View that process a POST with new car input

    Add new car information to database and get prediction results

    Returns:
        redirect to index page
    """
    if request.method == 'POST':
        try:
            car_manager.add_info(model=request.form['model'],
                                 year=request.form['year'],
                                 price=request.form['price'],
                                 transmission=request.form['transmission'],
                                 mileage=request.form['mileage'],
                                 fuelType=request.form['fuelType'],
                                 mpg=request.form['mpg'],
                                 engineSize=request.form['engineSize'])
            logger.info("New car info added: %s by %s", request.form['model'],
                        request.form['year'])
            return redirect(url_for('index'))

        except sqlite3.OperationalError as e:
            logger.error(
                "Error page returned. Not able to add song to local sqlite "
                "database: %s. Error: %s ",
                app.config['SQLALCHEMY_DATABASE_URI'], e)
            return render_template('error.html')
        except sqlalchemy.exc.OperationalError as e:
            logger.error(
                "Error page returned. Not able to add song to MySQL database: %s. "
                "Error: %s ",
                app.config['SQLALCHEMY_DATABASE_URI'], e)
            return render_template('error.html')

# @app.route('/result', methods=['POST'])
# def add_entry():
#     if request.method == 'POST':
#         user_input = request.form.to_dict()
#         user_input = str(user_input).lower()
#         try:
#             car_info = car_manager.session.query(Car).filter_by(input=user_input).limit(
#                 app.config["MAX_ROWS_SHOW"]).all()
#             if len(car_info) == 0:
#                 return render_template('not_found.html', user_input=user_input)
#             return render_template('index.html', car_info=car_info, user_input=user_input)
#         except sqlalchemy.exc.OperationalError:
#             traceback.print_exc()
#             logger.warning("Not able to display car information, error page returned")
#             return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"],
            host=app.config["HOST"])
