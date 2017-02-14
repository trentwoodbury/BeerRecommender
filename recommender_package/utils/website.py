''' Authors: Dylan Albrecht
             Trent Woodbury
    Date: December 18, 2016
    Some useful functions for working with data.
'''

import os
import cPickle as pickle
from collections import MutableMapping

import pandas as pd
import numpy as np
from unidecode import unidecode
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

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
        Store as graphlab compatible: None(NoneType) ... 'RwZ9MZ'(string) ...
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

def first_letter(cell):
    return str(cell[0]).lower()

def get_beer_names():
    #makes sorted list of all the beers
    beer_file = "beer_data_full.pkl"
    beer_path = os.path.join(DATA_DIR, beer_file)
    beer_df =  pd.read_pickle(beer_path)
    beer_df = feature_select(beer_df)
    beer_df.sort_values('name', inplace=True)
    names_and_ids = beer_df[['name', 'id']]
    return names_and_ids

def get_breweries():
    beer_file = "beer_data_full.pkl"
    beer_path = os.path.join(DATA_DIR, beer_file)
    beer_df = pd.read_pickle(beer_path)
    beer_df = feature_select(beer_df)
    beer_df.sort_values('name', inplace = True)
    breweries_and_ids = beer_df[['brewery_name', 'id']]
    return breweries_and_ids

def group_by_letter(names):
    alphabet = range(97, 123)
    groups = [[] for i in range(27)]
    for name in names:
        letter = ord(name[0][0].lower())
        if letter in range(97, 123):
            groups[122 - letter].append(name)
        else:
            groups[-1].append(name)
    return groups

def get_dfs():
    data_file = os.path.join(DATA_DIR, 'beer_data_full.pkl')

    with open(data_file, 'rb') as f:
        df = pickle.load(f)

    dfs = df.copy()

    return dfs

def get_dfs_train():
    data_file = os.path.join(DATA_DIR, 'beer_data_train.pkl')

    with open(data_file, 'rb') as f:
        df = pickle.load(f)

    dfs_train = df.copy()

    return dfs_train

def feature_select(dfs):
    global COLUMNS

    # Feature selection
    for col in dfs:
        if pd.isnull(dfs[col]).sum() > 5000:
            del dfs[col]

    # Simplest possible -- Drop NaN rows ((6928, 30)):
    dfs.dropna(axis=0, inplace=True)

    dfs['isOrganic'] = dfs['isOrganic'].apply(lambda x: True if x == 'Y'
                                                             else False)

    dfs = dfs[COLUMNS].copy()

    return dfs

def normalize(dfs, normalizer=None):

    columns = dfs.columns.tolist()
    index = dfs.index

    if normalizer:
        ss = normalizer
        norm_data = ss.transform(dfs)
    else:
        ss = StandardScaler()
        norm_data = ss.fit_transform(dfs)

    dfs_norm = pd.DataFrame(norm_data, index=index, columns=columns)

    return dfs_norm, ss

def vectorize(dfs, vectorizer=None):

    dfs['text'] = ""

    # Add all string columns together:
    for col in dfs:
        if col == 'text':
            continue

        if dfs[col].dtype == np.object:
            dfs['text'] += " " + dfs[col]
            del dfs[col]

    if vectorizer:
        tfidf = vectorizer
        vec_text = tfidf.transform(dfs['text'])
    else:
        tfidf = TfidfVectorizer(max_df=0.9, min_df=0.1, stop_words='english')
        vec_text = tfidf.fit_transform(dfs['text'])

    dfs_sparse = pd.DataFrame(vec_text.toarray(),
                              columns=tfidf.get_feature_names(),
                              index=dfs.index)
    dfs = pd.concat([dfs, dfs_sparse], axis=1)
    del dfs['text']

    return dfs, tfidf
