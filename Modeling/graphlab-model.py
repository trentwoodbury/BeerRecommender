''' Authors: Dylan Albrecht
             Trent Woodbury

    A simple graphlab model.
'''

import os
import sys
import cPickle as pickle

import pandas as pd
import numpy as np
import graphlab as gl

from utils import get_dfs
from utils import feature_select
from utils import normalize
from utils import vectorize


# XXX: THIS FUNCTION IS CURRENTLY NOT USED. NEEDS USERS/RATINGS.
def sim_rec(sf):

    # Fake/test/new data points:
    sfnew = sf[1:2]
    sfnew['style_fgMax'] = 1.5
    sfnew['id'] = 'p00p1'
    
    sfnew2 = sf[3:4]
    sfnew2['style_fgMax'] = 1.5
    sfnew2['id'] = 'p00p2'

    sf = sf.append(sfnew)
    sf = sf.append(sfnew2)

    # Train the similarity engine:
    similarity_model = gl.recommender.item_similarity_recommender.create(
                            sf,
                            item_id='id')

    # Recommendations:
    nn = similarity_model.get_similar_items(['p00p1', 'p00p2'])


if __name__ == '__main__':

    dfs = get_dfs()
    dfs = feature_select(dfs)
    dfs_train = dfs.copy()

    del dfs_train['id']
    dfs_train, tfidf_vec = vectorize(dfs_train)
    dfs_train, normalizer = normalize(dfs_train)
    dfs_train = pd.concat([dfs_train, dfs.id], axis=1)

    # SFrame
    sf = gl.SFrame(dfs)
    sf_train = gl.SFrame(dfs_train)
    knn = gl.nearest_neighbors.create(sf_train, label='id',
                                      method='brute_force',
                                      distance='euclidean')

    ###########
    # Testing

    print "TESTING..."

    # Fake/test/new data points:
    dfs_one = dfs[1:2].copy()
    dfs_one['style_fgMax'] = 1.01

    # Drop 'id' to transform and add back in for SFrame
    del dfs_one['id']
    dfs_one, _ = vectorize(dfs_one, vectorizer=tfidf_vec)
    dfs_one, _ = normalize(dfs_one, normalizer=normalizer)

    dfs_one['id'] = 'p00p1'

    sf_one = gl.SFrame(dfs_one)
    nn = knn.query(sf_one, label='id', k=1)

    if nn['reference_label'][0] == 'SJTtiL':
        print "Test Passed! Model is working."
    else:
        print "Test Failed!"

    # Another point test:
    pt_idx = np.random.randint(len(dfs))
    query_pt_pd = dfs[pt_idx:pt_idx+1].copy()

    del query_pt_pd['id']
    query_pt_pd, _ = vectorize(query_pt_pd, vectorizer=tfidf_vec)
    query_pt_pd, _ = normalize(query_pt_pd, normalizer=normalizer)
    query_pt_pd['id'] = 'p00p1'

    query_pt = gl.SFrame(query_pt_pd)
    query_pt['style_fgMin'] = np.nan

    print '=' * 40
    print "FINDING 5 MATCHES FOR: " + dfs.iloc[pt_idx]['name'] + " ("\
                                    + dfs.iloc[pt_idx]['style_name'] + ")"
    print '=' * 40

    ans = knn.query(query_pt, label='id', k=6)

    labels = ans['reference_label'][1:]

    for i, l in enumerate(labels):
        entry = sf[sf['id'] == l][0]
        print str(i+1) + ": " + entry['name'] + " (" + entry['style_name'] + ")"


    #####################################
    # Save Model and Feature selection:

    feature_file = os.path.join(os.pardir, 'Data', 'features_list.pkl')
    normalizer_file = os.path.join(os.pardir, 'Data', 'normalizer.pkl')
    vectorizer_file = os.path.join(os.pardir, 'Data', 'vectorizer.pkl')
    data_file = os.path.join(os.pardir, 'Data', 'beer_data_train.pkl')
    model_file = os.path.join(os.pardir, 'Data', 'graphlab_model.pkl')

    with open(feature_file, 'wb') as f:
        pickle.dump(dfs.columns.tolist(), f)

    with open(normalizer_file, 'wb') as f:
        pickle.dump(normalizer, f)

    with open(vectorizer_file, 'wb') as f:
        pickle.dump(tfidf_vec, f)

    with open(data_file, 'wb') as f:
        pickle.dump(dfs_train, f)

#    # only if we can actually pickle the object!
#    with open(model_file, 'wb') as f:
#        pickle.dump({'model': knn}, f)


##############
# End of File
##############
