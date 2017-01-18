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
    my_beers = []
    my_breweries = []

    for entry in beer_co_clean.find():
        my_beers.append(flatten(entry))
    for entry in breweries_clean.find():
        my_breweries.append(flatten(entry))

    ## Feature selections?
    df_beers = pd.DataFrame(my_beers)
    df_breweries = pd.DataFrame(my_breweries)

    #############
    # Transform

    # Get rid of mongo id
    del df_beers['_id']
    df_beers = convert_columns(df_beers)

    #Subset columns on df_beers and df_breweries
    df_beers = df_beers.loc[:, ['abv', 'description', 'style_description', 'style_ibuMax', 'id', 'isOrganic', 'name', 'style_name', 'nameDisplay', 'style_fgMax', 'style_fgMin']]
    df_breweries = df_breweries.loc[:, ['images_icon', 'name', 'website']]
    df_breweries.rename(columns = {"name": "brewery_name"}, inplace = True)
    df_breweries.loc[:,'images_icon'] = df_breweries['images_icon'].fillna(value = 'http://downloadicons.net/sites/default/files/beer-icons-46158.png')
    df_breweries = convert_columns(df_breweries)

    #Concatenate df_breweries and df_beers
    df_beers = pd.concat([df_beers, df_breweries], axis = 1)
    df_beers.drop_duplicates(inplace=True)

    ########
    # Save

    savefile = os.path.join(os.pardir, 'Data', 'beer_data_full.pkl')
    save_web = os.path.join(os.pardir, 'website', 'beer_data_full.pkl')


    with open(savefile, 'wb') as f:
        pickle.dump(df_beers, f, protocol=pickle.HIGHEST_PROTOCOL)
    with open(save_web, 'wb') as f:
        pickle.dump(df_beers, f, protocol=pickle.HIGHEST_PROTOCOL)
