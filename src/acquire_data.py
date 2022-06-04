"""
This module is for getting the input data
"""

import logging
import pandas as pd

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def import_data(path, columns=None):
    """Acquire the data and form a dataframe
        Args:
            path(str): the url to the raw data
            columns(list of str): the columns of raw data to be selected
        Returns:
            data (pd.Dataframe): bwm info raw data
    """
    logger.info("Start acquiring data")

    data = pd.read_csv(path)
    logger.info('Data loaded from path %s', path)

    if not isinstance(data, pd.DataFrame):
        raise TypeError("Provided argument `data` is not a Panda's DataFrame object")
    data = data[columns]
    logger.info("The columns for the model has been selected")

    return data
