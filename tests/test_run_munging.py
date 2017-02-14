import os
import sys
import cPickle as pickle

import pandas as pd

from package_context import recommender_package

from recommender_package.database.collection import CollectionManager
from recommender_package.utils.munging import convert_columns
from recommender_package.test_config import BEER_DB
from recommender_package.test_config import BBL_CO
from recommender_package.test_config import DATA_DIR
from recommender_package.test_config import DATA_FULL_PKL
from recommender_package.test_config import DATA_TRAIN_PKL
from recommender_package.test_config import COLUMNS


if __name__ == '__main__':

    # Mongo collection to DataFrame
    cm = CollectionManager(database_name=BEER_DB, collection_name=BBL_CO)
    bbl_co = cm.connect()
    entries_list = []
    for entry in bbl_co.find():
        entries_list.append(entry)

    df_beer = pd.DataFrame(entries_list)

    # Build training dataset:
    df_beer_train = df_beer[COLUMNS].copy()

    fill = 'http://downloadicons.net/sites/default/files/beer-icons-46158.png'
    df_beer_train.loc[:, 'breweries_images_icon'] = \
        df_beer_train['breweries_images_icon'].fillna(value=fill)

    df_beer_train = convert_columns(df_beer_train)
    df_beer_train.drop_duplicates(inplace=True)

    ##
    # Save to pickle

    savefile_full = os.path.join(DATA_DIR, DATA_FULL_PKL)
    with open(savefile_full, 'wb') as f:
        pickle.dump(df_beer, f, protocol=pickle.HIGHEST_PROTOCOL)

    savefile_train = os.path.join(DATA_DIR, DATA_TRAIN_PKL)
    with open(savefile_train, 'wb') as f:
        pickle.dump(df_beer_train, f, protocol=pickle.HIGHEST_PROTOCOL)
