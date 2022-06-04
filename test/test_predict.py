"""
This module is for testing predict.py
"""

import pytest
import pandas as pd
from src.predict import transform_input


def test_transform_input():
    """
    Happy path for testing the transform_input function
    """
    user_input = {'model': '5 Series',
                  'year': 2017,
                  'transmission': 'Semi-Auto',
                  'mileage': 67068,
                  'fuelType': 'Diesel',
                  'mpg': 60,
                  'engineSize': 20}
    df_true = pd.DataFrame([[0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 1.0000e+00,
                             0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0,
                             0, 1.0, 1.0, 0, 0,
                             0, 0, 2017, 67068, 60,
                             20]],
                           index=[0],
                           columns=['x0_1 Series', 'x0_2 Series', 'x0_3 Series', 'x0_4 Series',
                                    'x0_5 Series', 'x0_6 Series', 'x0_7 Series', 'x0_8 Series', 'x0_M2',
                                    'x0_M3', 'x0_M4', 'x0_M5', 'x0_M6', 'x0_X1', 'x0_X2', 'x0_X3', 'x0_X4',
                                    'x0_X5', 'x0_X6', 'x0_X7', 'x0_Z3', 'x0_Z4', 'x0_i3', 'x0_i8',
                                    'x1_Automatic', 'x1_Manual', 'x1_Semi-Auto', 'x2_Diesel', 'x2_Electric',
                                    'x2_Hybrid', 'x2_Other', 'x2_Petrol', 'year', 'mileage', 'mpg',
                                    'engineSize'])
    cat_col = ['model', 'transmission', 'fuelType']
    ohe_cols = ['x0_1 Series', 'x0_2 Series', 'x0_3 Series', 'x0_4 Series',
                'x0_5 Series', 'x0_6 Series', 'x0_7 Series', 'x0_8 Series', 'x0_M2',
                'x0_M3', 'x0_M4', 'x0_M5', 'x0_M6', 'x0_X1', 'x0_X2', 'x0_X3', 'x0_X4',
                'x0_X5', 'x0_X6', 'x0_X7', 'x0_Z3', 'x0_Z4', 'x0_i3', 'x0_i8',
                'x1_Automatic', 'x1_Manual', 'x1_Semi-Auto', 'x2_Diesel', 'x2_Electric',
                'x2_Hybrid', 'x2_Other', 'x2_Petrol', 'year', 'mileage', 'mpg',
                'engineSize']
    df_test = transform_input(user_input, cat_col, ohe_cols)
    pd.testing.assert_frame_equal(df_true, df_test)


def test_transform_input_non_dict():
    """
    Test when there is no dictionary provided
    """
    sample_input = 'I am not a dictionary'
    cat_col = ['model', 'transmission', 'fuelType']
    ohe_cols = ['x0_1 Series', 'x0_2 Series', 'x0_3 Series', 'x0_4 Series',
                'x0_5 Series', 'x0_6 Series', 'x0_7 Series', 'x0_8 Series', 'x0_M2',
                'x0_M3', 'x0_M4', 'x0_M5', 'x0_M6', 'x0_X1', 'x0_X2', 'x0_X3', 'x0_X4',
                'x0_X5', 'x0_X6', 'x0_X7', 'x0_Z3', 'x0_Z4', 'x0_i3', 'x0_i8',
                'x1_Automatic', 'x1_Manual', 'x1_Semi-Auto', 'x2_Diesel', 'x2_Electric',
                'x2_Hybrid', 'x2_Other', 'x2_Petrol', 'year', 'mileage', 'mpg',
                'engineSize']
    with pytest.raises(ValueError):
        transform_input(sample_input, cat_col, ohe_cols)
