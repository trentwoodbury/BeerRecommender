import numpy as np

from recommender_package.modeling.recommender import BeerTransformer
from recommender_package.modeling.recommender import BeerKNN
from recommender_package.utils.modeling import save_model
from recommender_package.utils.modeling import get_dfs
from recommender_package.utils.munging import raw_to_transform_data

if __name__ == '__main__':


    ###########################
    # Load and transform data
    dfs = get_dfs()

    dfs_transform = raw_to_transform_data(dfs)

    beer_transformer = BeerTransformer()
    dfs_train = beer_transformer.fit_transform(dfs_transform.copy())

    ########################
    # Train and save model

    beer_knn = BeerKNN(index=dfs_train.index.values)
    beer_knn.fit(dfs_train.values)

    save_model(beer_knn, beer_transformer, dfs_train)

    ##########################################################
    # Testing -- TODO: This will be part of the unit testing.
#    print "TESTING..."
#    dfs_one = dfs[1:2].copy()
#    dfs_one['style_fgMax'] = 1.01
#    dfs_one = raw_to_transform_data(dfs_one)
#    dfs_one = beer_transformer.transform(dfs_one)
#    indices = beer_knn.predict(dfs_one.values)
#    nn = dfs.iloc[indices[0], :]
#
#    if nn['id'][0] == 'SJTtiL':
#        print "Test Passed! Model is working."
#    else:
#        print "Test Failed!"

    # Another point test:
    pt_idx = np.random.randint(len(dfs))

    print '=' * 40
    print "FINDING 5 MATCHES FOR: " + dfs.iloc[pt_idx]['name'] + " ("\
                                    + dfs.iloc[pt_idx]['style_name'] + ")"
    print '=' * 40

    dfs_one = dfs.iloc[pt_idx:pt_idx+1].copy()
    dfs_one = raw_to_transform_data(dfs_one)
    dfs_one = beer_transformer.transform(dfs_one)
    indices = beer_knn.predict(dfs_one.values)
    nns = dfs_transform.loc[indices][1:]

    for i, r in enumerate(nns.iterrows()):
        print str(i+1) + ": " + r[1]['name'] + " (" + r[1]['style_name'] + ")"

