''' Authors: Dylan Albrecht
             Trent Woodbury

    Date: December 18, 2016

    Some useful functions for working with data.

'''
from collections import MutableMapping
import pandas as pd

from ..config import COLUMNS
from ..config import BEER_ID
from ..config import DROP_COLS

def flatten(d, parent_key='', sep='_'):
    ''' Recursive algorithm to flatten nested dictionaries, with keys
        created by joining with 'sep'.
        INPUT: dict, str, str
        OUTPUT: dict
    '''
    items = []

    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k

        if isinstance(v, MutableMapping):
            # Extend by sub keys -- enter recursive:
            items.extend(flatten(v, parent_key=new_key, sep=sep).items())
        else:
            items.append((new_key, v))

    return dict(items)

def convert_columns(df):
    ''' Take care of columns like: NaN(float) ... RwZ9MZ(unicode) ...
    #    Store as graphlab compatible: None(NoneType) ... 'RwZ9MZ'(string) ...
        Store as: '' ... 'RwZ9MZ'(string) ...
        INPUT: pd.DataFrame
        OUTPUT: pd.DataFrame
    '''
    for col in df:
        if df[col].dtype == np.object:
            df[col] = df[col].apply(lambda x: '' if type(x) == float \
                                                   else unidecode(x))

        # And convert 'float' columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')

    return df

def feature_select(dfs):
    global COLUMNS

    # Feature selection
    for col in dfs:
        if col not in COLUMNS or col in DROP_COLS:
            del dfs[col]

    # Simplest possible -- Drop NaN rows ((6928, 30)):
    dfs.dropna(axis=0, inplace=True)

    dfs['isOrganic'] = dfs['isOrganic'].apply(lambda x: True if x == 'Y'
                                                             else False)

    dfs = dfs[list(set(COLUMNS) - set(DROP_COLS))].copy()

    return dfs


def raw_to_transform_data(dfs_raw):
    dfs_transform = dfs_raw.groupby(BEER_ID).first().copy()
#    dfs.reset_index(inplace = True)
    dfs_transform = feature_select(dfs_transform)
    return dfs_transform
