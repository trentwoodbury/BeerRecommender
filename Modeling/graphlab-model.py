''' Authors: Dylan Albrecht

    A simple graphlab model.
'''

import os
import cPickle as pickle

import pandas as pd
import graphlab as gl


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

    # SFrame
    sf = gl.SFrame(dfs)

    knn = gl.nearest_neighbors.create(sf, label='id')

    ###########
    # Testing

    print "TESTING..."

    # Fake/test/new data points:
    sfnew = sf[1:2]
    sfnew['style_fgMax'] = 1.5
    sfnew['id'] = 'p00p1'
    
    nn = knn.query(sfnew, label='id', k=1)

    if nn['reference_label'][0] == 'SJTtiL':
        print "Test Passed! Model is working."
    else:
        print "Test Failed!"

    s_idx = np.random.randint(len(sf))
    query_pt = sf[s_idx:s_idx+1]
    print '=' * 40
    print "FINDING 5 MATCHES FOR: " + query_pt[0]['name'] + " ("\
                                    + query_pt[0]['style_name'] + ")"
    print '=' * 40

    ans = knn.query(query_pt, label='id', k=6)

    labels = ans['reference_label'][1:]

    for i, l in enumerate(labels):
        entry = sf[sf['id'] == l][0]
        print str(i) + ": " + entry['name'] + " (" + entry['style_name'] + ")"


##############
# End of File
##############
