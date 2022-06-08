"""
This module contains multiple functions that offers
user input transformation and prediction functionality
"""

import logging

import numpy
import pandas as pd
import typing
import pickle
from sklearn.preprocessing import OneHotEncoder

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def transform_input(ui_dict: dict,
                    cat_cols: typing.List[str],
                    ohe_cols: typing.List[str]) -> pd.DataFrame:
    """Transform the user input from the app to get predictions using the trained model
    Args:
        ui_dict (dict): a dictionary of user input, collected from the app
        cat_cols (:obj: `list`): a list of categorical columns in the initial input
        ohe_cols (:obj: `list`): a list of required columns in the transformed user input DataFrame
    Returns:
        test_df (:obj:`DataFrame <pandas.DataFrame>`): DataFrame that stores the transformed user input
    """
    # transform the user input into a pd Dataframe
    input_df = pd.DataFrame(ui_dict, index=[0])

    # Create a new dataframe to match the ohe_col names
    ohe_empty = pd.DataFrame(columns=ohe_cols)

    # ohe transform on the categorical columns
    ohe = OneHotEncoder()
    data1 = pd.DataFrame(ohe.fit_transform(input_df[cat_cols]).toarray(),
                         columns=ohe.get_feature_names())

    # merge the ohe data with all the input data
    merged_input = pd.concat([data1, input_df], axis=1).drop(cat_cols, axis=1)

    # Join the merged input data with the empty dataframe for training
    for col in ohe_empty.columns:
        if col not in merged_input.columns:
            ohe_empty[col] = 0
        else:
            ohe_empty[col] = merged_input[col]
    test_df = ohe_empty.fillna(0)

    return test_df


def get_prediction(test_df: pd.DataFrame,
                   model_path: str) -> numpy.ndarray:
    """Get car price prediction for new user input
    Args:
        test_df (:obj:`DataFrame <pandas.DataFrame>`): a DataFrame of the transformed user input
        model_path (str): the path to trained model;
            default is 'data/raw/rf.sav' (config.yaml)
    Returns:
        ypred (np.ndarray): the predicted price of the car from the user input
    """

    # load the pre-trained model
    with open(model_path, 'rb') as file:
        try:
            loaded_rf = pickle.load(file)
        except pickle.PickleError:
            logger.error("Error while loading trained model object.")
        else:
            logger.info('Loaded model from %s', model_path)

    # make prediction
    ypred = loaded_rf.predict(test_df)
    logger.info('The prediction has been made')

    return ypred
