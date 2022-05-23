"""
This module is for scoring the model
"""
import logging

import sklearn

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def score_model(rf, X_test):
    """make predictions on the test dataset based on the trained random forest model
        Args:
            rf (sklearn.ensemble._forest.RandomForestClassifier): the trained random forest model
            X_test (pd.Dataframe): Test dataset of X variables

        Returns:
            ypred(numpy.ndarray): predicted probability for test dataset
    """
    y_pred = rf.predict(X_test)
    logger.info("The prediction for test dataset has been generated")
    return y_pred
