"""
This module is for running the model pipeline
"""
import argparse
import logging

import yaml
import pandas as pd
import numpy as np
import pickle

import src.acquire_data as acquire
import src.get_features as feature
import src.split_data as split
import src.train_model as train
import src.score_model as score
import src.evaluation as evaluation

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger('run-pipeline')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Acquire, generate feature, and build model from car_info data")

    parser.add_argument('step', help='Which step to run',
                        choices=['acquire', 'prepare_feature', 'split', 'train', 'score', 'evaluate'])
    parser.add_argument('--input', '-i', nargs='+', default=None, help='Path to input data')
    parser.add_argument('--config', default='config/config.yaml', help='Path to configuration file')
    parser.add_argument('--output', '-o', nargs='+', default=None,
                        help='Path to save output CSV (optional, default = None)')

    args = parser.parse_args()

    # Load configuration file for parameters and tmo path
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    logger.info("Configuration file loaded from %s" % args.config)

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
                    with open(i,'rb') as f:
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
