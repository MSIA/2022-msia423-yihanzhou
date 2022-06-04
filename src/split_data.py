"""
This module is for splitting the data
"""

import logging
import sklearn
import sklearn.ensemble

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def train_test_split(input_data, ratio, random_state, target):
    """Split the train and test data
        Args:
            input_data(pd.Dataframe):dataframe of prepared_data.csv
            ratio(float):the train-test split ratio
            random_state(int): the random_state of split the data
            target (str): the target column name
        Returns:
            X_train: X variables of train dataset
            X_test: X variables of test dataset
            y_train: y variable of train dataset
            y_test: y variable of test dataset
        """
    # Extract the feature columns
    features = input_data.drop([target], axis=1)
    logger.info("Feature columns have been extracted")
    target = input_data[target]
    logger.info("Target column has been extracted")

    # Split the train and test data
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(features, target, test_size=ratio,
                                                                                random_state=random_state)
    logger.info("The data has been split into train and test")

    return X_train, X_test, y_train, y_test
