''' Authors: Dylan Albrecht
             Trent Woodbury

    A simple graphlab model.
'''

import os
import sys
import cPickle as pickle

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

from utils import get_dfs
from utils import feature_select
from utils import normalize
from utils import vectorize


# XXX: THIS FUNCTION IS CURRENTLY NOT USED. NEEDS USERS/RATINGS.
# def sim_rec(sf):
#
#     # Fake/test/new data points:
#     sfnew = sf[1:2]
#     sfnew['style_fgMax'] = 1.5
#     sfnew['id'] = 'p0p1'
#
#     sfnew2 = sf[3:4]
#     sfnew2['style_fgMax'] = 1.5
#     sfnew2['id'] = 'p0p2'
#
#     sf = sf.append(sfnew)
#     sf = sf.append(sfnew2)
#
#     # Train the similarity engine:
#     similarity_model = gl.recommender.item_similarity_recommender.create(
#                             sf,
#                             item_id='id')
#
#     # Recommendations:
#     nn = similarity_model.get_similar_items(['p0p1', 'p0p2'])

def get_data():
    dfs = get_dfs()
    dfs = feature_select(dfs)
    dfs_train = dfs.copy()

    del dfs_train['id']
    dfs_train, tfidf_vec = vectorize(dfs_train)
    dfs_train, normalizer = normalize(dfs_train)

    return dfs, dfs_train, normalizer, tfidf_vec

def train_knn(dfs, dfs_train, neighbors = 6 ):
    #INPUT: neighbors (number of neighbors, int), dfs_train (first output of get_data function)
    #OUPUT: knn (trained model)

    knn = NearestNeighbors(n_neighbors=6, algorithm='brute').fit(dfs_train)
    #dfs_train = pd.concat([dfs_train, dfs.id], axis=1)

    ###########
    # Testing
    print "TESTING..."

    # Fake/test/new data points:
    dfs_one = dfs[1:2].copy()
    del dfs_one['id']

    dfs_one['style_fgMax'] = 1.01

    dfs_one, _ = vectorize(dfs_one, vectorizer=tfidf_vec)
    dfs_one, _ = normalize(dfs_one, normalizer=normalizer)

    dist, ind = knn.kneighbors(dfs_one)

    nn = dfs[ind[0][0]:ind[0][1]]

    if nn['id'].iloc[0] == 'SJTtiL':
        print "Test Passed! Model is working."
    else:
        print "Test Failed!"

    # Another point test:
    pt_idx = np.random.randint(len(dfs))
    query_pt_pd = dfs.iloc[pt_idx:pt_idx+1].copy()

    del query_pt_pd['id']
    query_pt_pd, _ = vectorize(query_pt_pd, vectorizer=tfidf_vec)
    query_pt_pd, _ = normalize(query_pt_pd, normalizer=normalizer)

    print '=' * 40
    print "FINDING 5 MATCHES FOR: " + dfs.iloc[pt_idx]['name'] + " ("\
                                    + dfs.iloc[pt_idx]['style_name'] + ")"
    print '=' * 40

    dist, ind = knn.kneighbors(query_pt_pd)

    nns = dfs.iloc[ind[0]]

    for i, r in enumerate(nns.iterrows()):
        print str(i+1) + ": " + r[1]['name'] + " (" + r[1]['style_name'] + ")"

    return knn

def save_model(dfs_train, knn, normalizer, tfidf_vec):
    #INPUT: output of get_data and train_knn functions
    #OUTPUT: None. Saves model and data to "Data" folder

    data_file = os.path.join(os.pardir, 'Data', 'beer_data_train.pkl')
    model_file = os.path.join(os.pardir, 'Data', 'knn_model.pkl')

    with open(data_file, 'wb') as f:
        pickle.dump(dfs_train, f)
    # only if we can actually pickle the object!
    with open(model_file, 'wb') as f:
        pickle.dump({'knn': knn,
                     'normalizer': normalizer,
                     'vectorizer': tfidf_vec}, f)

if __name__ == '__main__':

    dfs, dfs_train, normalizer, tfidf_vec = get_data()
    knn = train_knn(dfs, dfs_train)
    save_model


##############
# End of File
##############
