"""Create database, upload the result table and delete the table in RDS"""
import argparse
import logging.config

from sqlalchemy.exc import ProgrammingError, OperationalError
from config.flaskconfig import SQLALCHEMY_DATABASE_URI
from src.bmw_db import CarManager, create_db


# Set up logging config
logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('rds-pipeline')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create defined tables in database")
    subparsers = parser.add_subparsers(dest='subparser_name')

    # Sub_parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create Database")
    sb_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLALCHEMY connection URI for the database.")

    # Sub_parser for ingesting the result data from a csv
    sb_ingest = subparsers.add_parser("ingest_result",
                                      description="Add the result data to database")
    sb_ingest.add_argument("--input_path",
                           default="data/result/test_result.csv",
                           help="result data")
    sb_ingest.add_argument("--engine_string",
                           default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI")

    #Sub_parser for delete the car_info table
    sb_delete = subparsers.add_parser("delete",
                                      description="Delete the Car Info table")
    sb_delete.add_argument("--delete", "-d",
                           default=False, action="store_true",
                           help="Delete current records from car_info table before create_all")
    sb_delete.add_argument("--engine_string",
                           default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI")

    args = parser.parse_args()
    sp_used = args.subparser_name
    if sp_used == 'create_db':
        try:
            create_db(args.engine_string)
            logger.info("The car_info table has been created")
        except ValueError as e:
            logger.error("Exiting. Please check database connection string.")
        except (ProgrammingError, OperationalError) as e:
            logger.error("Exiting. An error has occurred while making the database connection.")
        except Exception as e:
            logger.error("Other errors detected")
    elif sp_used == 'ingest_result':
        car = CarManager(engine_string=args.engine_string)
        car.add_price_result(args.input_path)
        logger.info("the result data has been ingested")
        car.close()
    elif sp_used == 'delete':
        try:
            logging.info("Attempting to truncate car_info table.")
            session = CarManager(engine_string=args.engine_string)
            session.delete_car_info()
            logger.info("car_info table has been truncated.")
        except ValueError as e:
            logger.error("Exiting. Please check database connection string.")
        except (ProgrammingError, OperationalError) as e:
            logger.error('An error has occurred while making the database connection.')
        except Exception as e:
            logger.error("Error occurred while attempting to truncate car_info table.")
        finally:
            session.close()
