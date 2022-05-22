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


def train_model(input_data, ratio, random_state, target, n_estimators, max_depth, save_path):
    """Train the random forest model and the get the evaluation
        Args:
            input_data(pd.Dataframe): the bmw car_info data generated by last step
            ratio (float): the train-test split ratio
            random_state(int): random_state for training the model
            target(str): the target variable of the prediction
            n_estimators(int):number of estimator used in Random forest model
            max_depth(int): max depth of the random forest model
            save_path(str): the path to save the results
        Returns:y_pred
    """
    # Extract the feature columns
    features = input_data.drop([target], axis=1)
    logger.info("Feature columns have been extracted")
    target = input_data[target]
    logger.info("Target column has been extracted")

    # Normalize the feature columns
    scaler = StandardScaler()
    features = scaler.fit_transform(features)
    logger.info("Target columns have been normalized")

    # Split the train and test data
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=ratio)
    logger.info("The data has been split into train and test")

    # Train the Random Forest Model
    rf = sklearn.ensemble.RandomForestRegressor(random_state=random_state, n_estimators=n_estimators,
                                                max_depth=max_depth)
    rf.fit(X_train, y_train)
    logger.info("The Random Forest Model has been trained")
    print('Random Forest Regressor Train Score is : %s ', rf.score(X_train, y_train))

    # Score the model:
    y_pred = rf.predict(X_test)
    logger.info("The prediction for test dataset has been generated")

    # Evaluation:
    r2 = metrics.r2_score(y_test, y_pred)
    mae = metrics.mean_absolute_error(y_test, y_pred)
    mse = metrics.mean_squared_error(y_test, y_pred)
    logger.info('Completed evaluation of the Random Forest Classifier')
    logger.info('Mean absolute error on test: %0.3f', mae)
    logger.info('Mean squared error on test: %0.3f', mse)

    try:
        result = pd.DataFrame({"R2": r2, "MAE": mae, "MSE": mse}, index=[0])
        result.to_csv(save_path, index=False)
        logger.info("Evaluation results saved to location: %s", save_path)
    except ValueError:
        logger.error("Failed to save the evaluation results because "
                     "the DataFrame of evaluation results cannot be appropriately called")

    return y_pred
