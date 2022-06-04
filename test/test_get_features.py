"""
The module for testing get_features.py
"""

import pytest
import pandas as pd

from src.get_features import get_features

df_in_values = [['5 Series', 2014, 11200, 'Automatic', 67068, 'Diesel', 57.6, 2.0],
                ['6 Series', 2018, 27000, 'Automatic', 14827, 'Petrol', 42.8, 2.0],
                ['5 Series', 2016, 16000, 'Automatic', 62794, 'Diesel', 51.4, 3.0],
                ['1 Series', 2017, 12750, 'Automatic', 26676, 'Diesel', 72.4, 1.5],
                ['7 Series', 2014, 14500, 'Automatic', 39554, 'Diesel', 50.4, 3.0]]
df_in_index = range(0, 5)
df_in_columns = ['model', 'year', 'price', 'transmission', 'mileage', 'fuelType', 'mpg',
                 'engineSize']
df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)


def test_get_features_happy():
    """
    Test the get_features happy for expected behavior
    """
    df_test = get_features(df_in, ['model', 'transmission', 'fuelType'])
    df_true = pd.DataFrame([[0.0000e+00, 1.0000e+00, 0.0000e+00, 0.0000e+00, 1.0000e+00,
                             1.0000e+00, 0.0000e+00, 2014, 11200, 67068,
                             5.7600e+01, 2.0000e+00],
                            [0.0000e+00, 0.0000e+00, 1.0000e+00, 0.0000e+00, 1.0000e+00,
                             0.0000e+00, 1.0000e+00, 2018, 27000, 14827,
                             4.2800e+01, 2.0000e+00],
                            [0.0000e+00, 1.0000e+00, 0.0000e+00, 0.0000e+00, 1.0000e+00,
                             1.0000e+00, 0.0000e+00, 2016, 16000, 62794,
                             5.1400e+01, 3.0000e+00],
                            [1.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 1.0000e+00,
                             1.0000e+00, 0.0000e+00, 2017, 12750, 26676,
                             7.2400e+01, 1.5000e+00],
                            [0.0000e+00, 0.0000e+00, 0.0000e+00, 1.0000e+00, 1.0000e+00,
                             1.0000e+00, 0.0000e+00, 2014, 14500, 39554,
                             5.0400e+01, 3.0000e+00]],
                           index=range(0, 5),
                           columns=['x0_1 Series', 'x0_5 Series', 'x0_6 Series', 'x0_7 Series',
                                    'x1_Automatic', 'x2_Diesel', 'x2_Petrol', 'year', 'price', 'mileage',
                                    'mpg', 'engineSize'])
    pd.testing.assert_frame_equal(df_true, df_test)


def test_get_features_non_df():
    """
    Test when dataframe is not provided
    return: If a dataframe is not provided, we expect the function to raise a Type Error
    """
    df_in_non_df = 'I am not a DataFrame'
    with pytest.raises(TypeError):
        get_features(df_in_non_df,  ['model', 'transmission', 'fuelType'])

