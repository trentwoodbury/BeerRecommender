import numpy as np

from package_context import recommender_package

from recommender_package.modeling.recommender import BeerTransformer
from recommender_package.modeling.recommender import BeerKNN
from recommender_package.utils.modeling import save_model
from recommender_package.utils.modeling import get_dfs_train
from recommender_package.utils.munging import raw_to_transform_data

# Load test configuration:
from recommender_package.test_config import DATA_DIR
from recommender_package.test_config import DATA_TRAIN_PKL
from recommender_package.test_config import RECOMMENDER_MODEL_PKL



def print_test_matches(dfs, beer_transformer, beer_knn):

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


if __name__ == '__main__':


    ###########################
    # Load and transform data
    dfs_train = get_dfs_train(directory=DATA_DIR, filename=DATA_TRAIN_PKL)

    # Transform the data into a format for the BeerTransformer
    # -- Groupby beer id, take first
    # -- Feature select, based on COLUMNS in the config
    dfs_transform = raw_to_transform_data(dfs_train)

    beer_transformer = BeerTransformer()
    dfs_train_trans = beer_transformer.fit_transform(dfs_transform.copy())

    ########################
    # Train and save model

    beer_knn = BeerKNN(index=dfs_train_trans.index.values)
    beer_knn.fit(dfs_train_trans.values)

    save_model(beer_knn, beer_transformer, dfs_train_trans,
               directory=DATA_DIR, filename=RECOMMENDER_MODEL_PKL)

    ##################
    # Print test

    print_test_matches(dfs_train, beer_transformer, beer_knn)

###############
# End of File
###############
