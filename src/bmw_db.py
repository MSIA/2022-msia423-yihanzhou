"""Creates and ingests data into a table of information for the BMW."""
import typing
import logging

import flask
import pandas as pd
import sqlalchemy
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

# Set up logging config
logging.basicConfig(format='%(asctime)s%(name)-12s%(levelname)-8s%(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.DEBUG)
logger = logging.getLogger(__name__)

Base = declarative_base()


# Create a db session
class Car(Base):
    """
    Creates a data model for the database to be set up for capturing car information.
    """

    __tablename__ = "car_info"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    model = sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=False)
    year = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=False)
    transmission = sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=False)
    mileage = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=False)
    fuelType = sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=False)
    tax = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=False)
    mpg = sqlalchemy.Column(sqlalchemy.Float, unique=False, nullable=False)
    engineSize = sqlalchemy.Column(sqlalchemy.Float, unique=False, nullable=False)

    logger.info("Data table created")

    def __repr__(self):
        return f'Car model: {self.model}, built in: {self.year}, with mileage: {self.mileage}'


def create_db(engine_string: str = None) -> None:
    """
    Create database from provided engine string

    Args:
        engine_string (str): SQLAlchemy engine string specifying which database to write to

    Returns: None
    """
    if engine_string is None:
        logger.error('No ENGINE_STRING provided')
        raise ValueError("`ENGINE_STRING` must be provided")
    #else:
    engine = sqlalchemy.create_engine(engine_string)

    try:
        Base.metadata.create_all(engine)
    except sqlalchemy.exc.OperationalError:
        message = ('You might have connection error. Have you configured \n'
                   'SQLALCHEMY_DATABASE_URI variable correctly and connect to Northwestern VPN?')
        logger.error("Could not connect to database!")
        logger.error('%s', message)
    else:
        logger.info("Database created!")


class CarManager:
    """
    Creates a SQLAlchemy connection to the bmw information table.

    Args:
        app (:obj:`flask.app.Flask`): Flask app object for when connecting from
            within a Flask app. Optional.
        engine_string (str): SQLAlchemy engine string specifying which database
            to write to. Follows the format
    """

    def __init__(self, app: typing.Optional[flask.app.Flask] = None,
                 engine_string: typing.Optional[str] = None):
        """
        Args:
            app (Flask): Flask app
            engine_string (str): Engine String
        """
        if app:
            self.database = SQLAlchemy(app)
            self.session = self.database.session
        elif engine_string:
            engine = sqlalchemy.create_engine(engine_string)
            session_maker = sessionmaker(bind=engine)
            self.session = session_maker()
        else:
            raise ValueError("Need either an engine string or a Flask app to initialize")

    def add_price_result(self, input_path: str):
        """
        Create the result table in RDS

        Args:
            input_path (string): the path of the result data
        Returns:
            None
        """

        session = self.session
        logger.info("Session has been initialized")
        car_list = []
        data_list = pd.read_csv(input_path).to_dict(orient='records')
        logger.info("Result data has been uploaded")

        for data in data_list:
            car_list.append(Car(**data))

        try:
            session.add_all(car_list)
            session.commit()
        except sqlalchemy.exc.OperationalError:
            logger.error('You might have connection error')
            logger.error("The original error message is: ", exc_info=True)
        else:
            logger.info("There are %s records added to the table", len(car_list))

    def delete_car_info(self) -> None:
        """
        Deletes car info table if re-runing and run into unique key error.
        """
        session = self.session
        session.execute('DELETE FROM car_info')
        try:
            session.commit()
        except sqlalchemy.exc.OperationalError:
            logger.error('You might have connection error')
        else:
            logger.info("Delete successfully")

    def close(self) -> None:
        """
        Closes SQLAlchemy session

        Returns: None
        """
        self.session.close()
        logger.info("Session closed")

