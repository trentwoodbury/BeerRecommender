''' Authors: Dylan Albrecht
             Trent Woodbury

    Date: December 25, 2016

    
    Tests loading a mongo entry and runs it through the graphlab model.
    Prints the matches.

'''
import os
import cPickle as pickle

import pandas as pd
import numpy as np
from unidecode import unidecode
import graphlab as gl

from utils import connect_mongo
from utils import flatten
from utils import convert_columns


def get_dfs():
    data_file = os.path.join(os.pardir, 'Data', 'beer_data_full.pkl')

    with open(data_file, 'rb') as f:
        df = pickle.load(f)

    dfs = df.copy()

    # Feature selection
    for col in dfs:
        if pd.isnull(dfs[col]).sum() > 5000:
            del dfs[col]

    # Simplest possible -- Drop NaN rows ((6928, 30)):
    dfs.dropna(axis=0, inplace=True)

    return dfs


if __name__ == '__main__':

    #########
    # Load
    beer_co_clean = connect_mongo()

    # training data:
    dfs_train = get_dfs()

    #########################
    # Load mongo data point

    one = beer_co_clean.find_one()
    df = pd.DataFrame([flatten(one)])

    del df['_id']
    df = convert_columns(df)

    feature_file = os.path.join(os.pardir, 'Data', 'features_list.pkl')
    with open(feature_file, 'rb') as f:
        columns = pickle.load(f)

    dfs_point = df[columns]

    # ensure the same types:
    for col in dfs_point:
        dfs_point.loc[:,col] = dfs_point[col].astype(dfs_train[col].dtype)

    ##############
    # Load Model

    sf = gl.SFrame(dfs_train)
    knn = gl.nearest_neighbors.create(sf, label='id')
    query_pt = gl.SFrame(dfs_point)

    print '=' * 40
    print "FINDING 5 MATCHES FOR: " + query_pt[0]['name'] + " ("\
                                    + query_pt[0]['style_name'] + ")"
    print '=' * 40

    ans = knn.query(query_pt, label='id', k=6)

    labels = ans['reference_label'][1:]

    for i, l in enumerate(labels):
        entry = sf[sf['id'] == l][0]
        print str(i) + ": " + entry['name'] + " (" + entry['style_name'] + ")"
