''' Authors: Dylan Albrecht

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
from pymongo.errors import ServerSelectionTimeoutError


def flatten(d, parent_key='', sep='_'):
    ''' Recursive algorithm to flatten nested dictionaries, with keys
        created by joining with 'sep'.
        INPUT: dict, str, str
        OUTPUT: dict
    '''
    items = []

    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k

        if isinstance(v, collections.MutableMapping):
            # Extend by sub keys -- enter recursive:
            items.extend(flatten(v, parent_key=new_key, sep=sep).items())
        else:
            items.append((new_key, v))

    return dict(items)


if __name__ == '__main__':

    ########
    # Load

    MONGO_USERNAME = os.environ['MONGO_USERNAME']
    MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
    MONGO_HOSTNAME = os.environ['MONGO_HOSTNAME']

    # Check server:
    try:
        address = 'mongodb://'
        address += MONGO_USERNAME + ':'
        address += MONGO_PASSWORD + '@'
        address += MONGO_HOSTNAME
        cli = MongoClient(address, serverSelectionTimeoutMS=100)
        cli.server_info()

    except ServerSelectionTimeoutError as e:
        print "Server error!  (Is it plugged in?): "
        print e
        raise e
    
    raw = 'craft_beers_raw'
    clean = 'craft_beers'

    db = cli['beer_db']
    cols = db.collection_names()

    # Check for collections:
    if raw not in cols:
        print raw + ' does not exists yet! Run web-scraper first!'
        sys.exit()

    if clean not in cols:
        print clean + ' does not exists! Run raw_to_clean.py first!'
        sys.exit()

    beer_co_clean = db['craft_beers']

    # Add entries to Pandas dataframe:
    mydata = []
    for entry in beer_co_clean.find():
        mydata.append(flatten(entry))

    ## Feature selections?
    df = pd.DataFrame(mydata)

    #############
    # Transform

    # Get rid of mongo id
    del df['_id']

    # Take care of columns like: NaN(float) ... RwZ9MZ(unicode) ...
    # Store as graphlab compatible: None(NoneType) ... 'RwZ9MZ'(string) ... 
    for col in df:
        if df[col].dtype == np.object:
            df[col] = df[col].apply(lambda x: None if type(x) == float \
                                                else unidecode(x))

        # And convert 'float' columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')

    df.drop_duplicates(inplace=True)

    ########
    # Save

    savefile = os.path.join(os.pardir, 'Data', 'beer_data_full.pkl')

    with open(savefile, 'wb') as f:
        pickle.dump(df, f, protocol=pickle.HIGHEST_PROTOCOL)



