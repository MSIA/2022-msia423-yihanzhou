"""
This module is for running the model pipeline
"""
import argparse
import logging
import yaml
import pandas as pd

import src.acquire_data as acquire
import src.get_features as feature
import src.train_model as model

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger('run-pipeline')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Acquire, generate feature, and build model from car_info data")

    parser.add_argument('step', help='Which step to run', choices=['acquire', 'feature', 'model'])
    parser.add_argument('--input', '-i', default=None, help='Path to input data')
    parser.add_argument('--config', default='config/config.yaml', help='Path to configuration file')
    parser.add_argument('--output', '-o', default=None, help='Path to save output CSV (optional, default = None)')

    args = parser.parse_args()

    # Load configuration file for parameters and tmo path
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    logger.info("Configuration file loaded from %s" % args.config)

    if args.input is not None:
        input = pd.read_csv(args.input)
        logger.info('Input data loaded from %s', args.input)

    if args.step == 'acquire':
        output = acquire.import_data(**config['acquire_data'])
    elif args.step == 'feature':
        output = feature.get_features(input, **config['get_features'])
    elif args.step == 'model':
        output = model.train_model(input, **config['train_model'])

    if args.output is not None:
        output.to_csv(args.output, index=False)
        logger.info("Output saved to %s" % args.output)