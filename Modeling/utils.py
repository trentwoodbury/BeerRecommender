''' Authors: Dylan Albrecht
             Trent Woodbury

    Date: December 18, 2016

    Some useful functions for working with data.

'''

import os
from collections import MutableMapping

import pandas as pd
import numpy as np
from unidecode import unidecode
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


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


def connect_mongo():
    ########
    # Load

    MONGO_USERNAME = os.environ['MONGO_USERNAME']
    MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
    MONGO_HOSTNAME = os.environ['MONGO_HOSTNAME']

    # Check server:
    try:
        address = 'mongodb://'
        address += MONGO_USERNAME + ':'
        address += MONGO_PASSWORD + '@'
        address += MONGO_HOSTNAME
        cli = MongoClient(address, serverSelectionTimeoutMS=100)
        cli.server_info()

    except ServerSelectionTimeoutError as e:
        print "Server error!  (Is it plugged in?): "
        print e
        raise e
    
    raw = 'craft_beers_raw'
    clean = 'craft_beers'

    db = cli['beer_db']
    cols = db.collection_names()

    # Check for collections:
    if raw not in cols:
        print raw + ' does not exists yet! Run web-scraper first!'
        sys.exit()

    if clean not in cols:
        print clean + ' does not exists! Run raw_to_clean.py first!'
        sys.exit()

    beer_co_clean = db['craft_beers']

    return beer_co_clean


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
    # Take care of columns like: NaN(float) ... RwZ9MZ(unicode) ...
    # Store as graphlab compatible: None(NoneType) ... 'RwZ9MZ'(string) ... 
    for col in df:
        if df[col].dtype == np.object:
            df[col] = df[col].apply(lambda x: None if type(x) == float \
                                                   else unidecode(x))

        # And convert 'float' columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')

    return df
