"""
Configures the subparsers for receiving command line arguments for each
 stage in the model pipeline and orchestrates their execution.
 """
import argparse
import logging.config

import yaml
import pandas as pd
import pickle
import numpy as np

from sqlalchemy.exc import ProgrammingError, OperationalError
from src.bmw_db import CarManager, create_db
from src.s3 import upload_file_to_s3, download_file_from_s3
import src.acquire_data as acquire
import src.get_features as feature
import src.split_data as split
import src.train_model as train
import src.score_model as score
import src.evaluation as evaluation

from config.flaskconfig import SQLALCHEMY_DATABASE_URI

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('car-price-application-pipeline')

if __name__ == '__main__':

    # Add parsers for both creating a database and adding car information to it
    parser = argparse.ArgumentParser(
        description="Create and/or add data to database")
    subparsers = parser.add_subparsers(dest='subparser_name')

    # Sub-parser for creating a database
    sp_create = subparsers.add_parser("create_db",
                                      description="Create database")
    sp_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    # Sub-parser for uploading data to s3
    sb_upload = subparsers.add_parser('upload_file_to_s3', help='Upload raw data to s3')
    sb_upload.add_argument('--s3_path',
                           default='s3://2022-msia423-zhou-yihan/raw/bmw.csv',
                           help='s3 data path to upload data')
    sb_upload.add_argument('--local_path', default='./data/raw/bmw.csv',
                           help='local data path to store or upload data')

    # Sub-parser for downloading data from s3
    sb_download = subparsers.add_parser('download_file_from_s3', help='Download raw data from s3')
    sb_download.add_argument('--s3_path',
                             default='s3://2022-msia423-zhou-yihan/raw/bmw.csv',
                             help='s3 path to download the data')
    sb_download.add_argument('--local_path', default='./data/raw/bmw.csv',
                             help='local data path to store or upload data')

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser('ingest',
                                      description='Add data to database')
    sb_ingest.add_argument('--id', help='ID of car information')
    sb_ingest.add_argument('--model', help='Model type of the car')
    sb_ingest.add_argument('--year', help='Year of the car made')
    sb_ingest.add_argument('--transmission', help='Transmission type of the car')
    sb_ingest.add_argument('--mileage', help='The mileage used for the car')
    sb_ingest.add_argument('--fuelType', help='The fuel Type of the car')
    sb_ingest.add_argument('--mpg', help='The miles per gallon of the car')
    sb_ingest.add_argument('--engineSize', help='The size of the engine of the car')
    sb_ingest.add_argument("--engine_string",
                           default='sqlite:///data/msia423_db.db',
                           help="SQLAlchemy connection URI")

    # Sub-parser for delete the car_info table
    sb_delete = subparsers.add_parser('delete',
                                      description='Delete the Car info table')
    sb_delete.add_argument('--delete', '-d',
                           default=False,
                           action='store_true',
                           help='Delete current records from car_info table')
    sb_delete.add_argument("--engine_string",
                           default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI")

    ## Sub-parser for running the model pipeline:
    sb_pipeline = subparsers.add_parser('run_model_pipeline',
                                        description='Acquire, generate features, and build models from the car_info dataset')
    sb_pipeline.add_argument('step', help='Which step to run',
                        choices=['acquire', 'prepare_feature', 'split', 'train', 'score', 'evaluate'])
    sb_pipeline.add_argument('--input', '-i', nargs='+', default=None, help='Path to input data')
    sb_pipeline.add_argument('--config', default='config/config.yaml', help='Path to configuration file')
    sb_pipeline.add_argument('--output', '-o', nargs='+', default=None,
                        help='Path to save output CSV (optional, default = None)')

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

    elif sp_used == 'ingest':
        car = CarManager(engine_string=args.engine_string)
        car.add_info(args.id,
                     args.model,
                     args.year,
                     args.transmission,
                     args.mileage,
                     args.fuelType,
                     args.mpg,
                     args.engineSize)
        logger.info('The new car information data has been ingested')
        logger.info('The new information has been store to %s', args.engine_string)
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

    elif sp_used == 'upload_file_to_s3':
        upload_file_to_s3(args.local_path, args.s3_path)
    elif sp_used == 'download_file_from_s3':
        download_file_from_s3(args.local_path, args.s3_path)

    elif sp_used == 'run_model_pipeline':
        # Load configuration file for parameters and path
        try:
            with open(args.config, 'r') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                logger.info("Configuration file loaded from %s" % args.config)
        except FileNotFoundError:
            logger.error('Configuration file from %s is not found' % args.config)
        if args.input is not None:
            if len(args.input) == 1:
                input = pd.read_csv(args.input[0])
                logger.info('Input data loaded from %s', args.input)
            else:
                inputs = []
                for i in args.input:
                    # if the type of the file is pandas dataframe
                    if i.endswith('.csv'):
                        input = pd.read_csv(i)
                    # if the type of the file is a model
                    elif i.endswith('.sav'):
                        input = pickle.load(open(i, 'rb'))
                    # if the type of the file is a pandas series
                    elif i.endswith('.pkl'):
                        input = pd.read_pickle(i)
                    # if the type of the file is a numpy nparray
                    elif i.endswith('.npy'):
                        with open(i, 'rb') as f:
                            input = np.load(f, allow_pickle=True)
                    inputs.append(input)
                    logger.info('Input data loaded from %s', i)

        if args.step == 'acquire':
            output = acquire.import_data(**config['acquire_data'])
        elif args.step == 'prepare_feature':
            output = feature.get_features(input, **config['get_features'])
        elif args.step == 'split':
            output1, output2, output3, output4 = split.train_test_split(input, **config['split_data'])
            output = [output1, output2, output3, output4]
        elif args.step == 'train':
            output = train.train_model(inputs[0], inputs[1], **config['train_model'])
        elif args.step == 'score':
            output = score.score_model(inputs[0], inputs[1])
        elif args.step == 'evaluate':
            output = evaluation.evaluation(inputs[0], inputs[1])

            # Save the output to the path
        if args.output is not None:
            if len(args.output) == 1:
                if type(output) == pd.core.frame.DataFrame:
                    output.to_csv(args.output[0], index=False)
                elif type(output) == pd.core.series.Series:
                    output.to_pickle(args.output[0])
                else:
                    pickle.dump(output, open(args.output[0], 'wb'))
                logger.info("Output has been save to %s" % args.output[0])

            else:
                for i in range(len(output)):
                    if type(output[i]) == pd.core.frame.DataFrame:
                        output[i].to_csv(args.output[i], index=False)
                    elif type(output[i]) == pd.core.series.Series:
                        output[i].to_pickle(args.output[i])
                    else:
                        with open(args.output[i], 'wb') as f:
                            np.save(f, output[i])
                    logger.info("Output has been save to %s" % args.output[i])
    else:
        parser.print_help()
