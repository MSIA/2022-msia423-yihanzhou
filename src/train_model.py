"""
This module is for training the model and get the result
"""

import logging
import sklearn
import sklearn.ensemble
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import metrics

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def train_model(X_train, y_train, n_estimators, max_depth, random_state):
    """Train the random forest model and the get the evaluation
        Args:
            X_train(pd.Dataframe): Training set of X variables
            y_train(pd.Series): Training set of Y variable
            n_estimators(int):number of estimator used in Random forest model
            max_depth(int): max depth of the random forest model
            random_state(int): random_state for training the model
        Returns:
            rf(sklearn.ensemble._forest.RandomForestClassifier): the trained random forest model
    """

    # Train the Random Forest Model
    rf = sklearn.ensemble.RandomForestRegressor(random_state=random_state, n_estimators=n_estimators,
                                                max_depth=max_depth)
    rf.fit(X_train, y_train)
    logger.info("The Random Forest Model has been trained")
    print('Random Forest Regressor Train Score is : %s ', rf.score(X_train, y_train))

    return rf
