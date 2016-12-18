''' Authors: Dylan Albrecht

    Date: December 18, 2016

    Some useful functions for working with data.

'''


import pandas as pd


def display_non_nan(df):
    ''' Displays a sampling of the non null values of all the columns
        Format: 'column1  TYPE: float  Value(float): 1.0'
                'column2  TYPE: object  Value(str): Eating cake is...'
                        .               .               .
                        .               .               .
                        .               .               .
        INPUT: pd.DataFrame
        OUTPUT: None
    '''
    for col in df:
        dfs = df[col].copy()
        st = "{0}  TYPE: {1}  VALUE({2}): {3}"
        col_type = df[col].dtype
        val = dfs[~pd.isnull(dfs)].iloc[0]
        val_type = type(val)
        print st.format(col, col_type, val_type, val)

