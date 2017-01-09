''' Authors: Dylan Albrecht
             Trent Woodbury

    Date: December 18, 2016

    This script takes the mongo database, where each entry is a single craft
    beer, and flattens the dictionary into a Pandas DataFrame.

    This dataframe is saved to disk, in 'Data'.

    TODO: What features do we want to use?

'''
import os
import collections
import cPickle as pickle

import pandas as pd
import numpy as np
from unidecode import unidecode
from pymongo import MongoClient

from utils import connect_breweries
from utils import connect_mongo
from utils import flatten
from utils import convert_columns


if __name__ == '__main__':

    ########
    # Load
    beer_co_clean = connect_mongo()
    breweries_clean = connect_breweries()

    # Add entries to Pandas dataframe:
    mybeers = []
    for entry in beer_co_clean.find():
        mybeers.append(flatten(entry))

    ## Feature selections?
    df = pd.DataFrame(mybeers)

    #############
    # Transform

    # Get rid of mongo id
    del df['_id']
    df = convert_columns(df)
    df.drop_duplicates(inplace=True)

    ########
    # Save

    savefile = os.path.join(os.pardir, 'Data', 'beer_data_full.pkl')
    save_web = os.path.join(os.pardir, 'website', 'beer_data_full.pkl')


    with open(savefile, 'wb') as f:
        pickle.dump(df, f, protocol=pickle.HIGHEST_PROTOCOL)
    with open(save_web, 'wb') as f:
        pickle.dump(df, f, protocol=pickle.HIGHEST_PROTOCOL)
