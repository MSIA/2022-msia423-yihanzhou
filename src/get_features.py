"""
The module is to featurize the data and get the predictive and target variables
"""
import logging
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_features(data, cat_col):
    """
    Convert the categorical variables into dummy variables
    Args:
        data(pd.Dataframe): the raw data
        cat_col(list of str): the categorical columns
    Returns:
        input_data(pd.Dataframe): the input data for training the model
    """

    # Find the categorical columns
    # cat_col = [col for col in data.columns if data[col].dtype == 'object']

    # Convert categorical columns using One hot encoder
    ohe = OneHotEncoder()
    ohe_features = pd.DataFrame(ohe.fit_transform(data[cat_col]).toarray(),
                                columns=ohe.get_feature_names())

    input_data = pd.concat([ohe_features, data], axis=1).drop(cat_col, axis=1)

    return input_data
