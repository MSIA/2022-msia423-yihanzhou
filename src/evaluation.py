"""
This module is for evaluating the model result
"""

import logging

import pandas as pd

import sklearn
from sklearn import metrics

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def evaluation(y_test, y_pred):
    """evaluate the performance of the random forest model
        Args:
            y_test(pd.Series): the test dataset of Y variable
            y_pred(np.ndarray): the test prediction results
        Returns:
            result(pd.Dataframe): The result of the model
    """
    r2 = metrics.r2_score(y_test, y_pred)
    mae = metrics.mean_absolute_error(y_test, y_pred)
    mse = metrics.mean_squared_error(y_test, y_pred)
    logger.info('Completed evaluation of the Random Forest Classifier')
    logger.info('R Squared on test: %0.3f', r2)
    logger.info('Mean absolute error on test: %0.3f', mae)
    logger.info('Mean squared error on test: %0.3f', mse)

    result = pd.DataFrame({"R2": r2, "MAE": mae, "MSE": mse}, index=[0])

    return result
