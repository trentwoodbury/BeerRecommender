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
from utils import get_dfs
from utils import feature_select
from utils import COLUMNS


if __name__ == '__main__':

    #########
    # Load
    beer_co_clean = connect_mongo()

    # training data:
    dfs_train = get_dfs()
    dfs_train = feature_select(dfs_train)

    #########################
    # Load mongo data point
    # -- in the future this would be a post request.

    one = beer_co_clean.find_one()
    df = pd.DataFrame([flatten(one)])

    del df['_id']
    df = convert_columns(df)

    dfs_point = df[COLUMNS].copy()

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
        
###############
# End of File
###############
