''' Authors: Dylan Albrecht
             Trent Woodbury

    Date: December 18, 2016

    Some useful functions for working with data.

'''

import os
import cPickle as pickle

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

from ..config import COLUMNS
from ..config import DATA_DIR
from ..config import DATA_FULL_PKL
from ..config import DATA_TRAIN_PKL
from ..config import RECOMMENDER_MODEL_PKL


def get_dfs(directory=DATA_DIR, filename=DATA_FULL_PKL):
    data_file = os.path.join(directory, filename)

    with open(data_file, 'rb') as f:
        df = pickle.load(f)

    dfs = df.copy()

    return dfs


def get_dfs_train(directory=DATA_DIR, filename=DATA_TRAIN_PKL):
    data_file = os.path.join(directory, filename)

    with open(data_file, 'rb') as f:
        df = pickle.load(f)

    dfs_train = df.copy()

    return dfs_train


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


def save_model(recommender, transformer, data,
               directory=DATA_DIR,
               filename=RECOMMENDER_MODEL_PKL):
    model_file = os.path.join(directory, filename)

    with open(model_file, 'wb') as f:
        pickle.dump({'recommender': recommender,
                     'transformer': transformer,
                     'data': data}, f)

def load_model(directory=DATA_DIR,
               filename=RECOMMENDER_MODEL_PKL):
    model_file = os.path.join(directory, filename)

    with open(model_file, 'rb') as f:
        model = pickle.load(f)

    recommender = model['recommender']
    transformer = model['transformer']
    data = model['data']

    return recommender, transformer, data


