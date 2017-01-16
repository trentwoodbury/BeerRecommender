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
    my_beers = []
    my_breweries = []

    for entry in beer_co_clean.find():
        my_beers.append(flatten(entry))
    for entry in breweries_clean.find():
        my_breweries.append(flatten(entry))

    ## Feature selections?
    df_beers = pd.DataFrame(my_beers)
    df_breweries = pd.DataFrame(my_breweries)


    # LOCATIONS HACK -- should probably re-grab data:
    #   beer_id -> [list of brewery ids, with location data]
    #   unique id could be '_'.join([beerid, breweryid, locationid])
    locations_file = os.path.join(os.pardir, 'Data', 'test_locations.pkl')
    with open(locations_file, 'rb') as f:
        df_locations = pickle.load(f)

    df_locations_merge = df_locations.groupby('brewery_id').first().copy()

#    df_beers.rename(columns={'id': 'beer_id'}, inplace=True)
    df_breweries.rename(columns={"name": "breweryName",
                                 'website': 'breweryWebsite',
                                 'description': 'brewery_description',
                                 'isOrganic': 'brewery_isOrganic',
                                 'id': 'brewery_id'},
                        inplace=True)
    filler_image = 'http://downloadicons.net/sites/default/files/' \
                    + 'beer-icons-46158.png'
    df_breweries.loc[:,'images_icon'] = df_breweries['images_icon'].fillna(
                    value=filler_image)
    df_locations_merge.rename(columns={'id': 'locations_id',
                                       'name': 'locations_brewery_name'},
                              inplace=True)

    df_merged = pd.merge(df_breweries, df_locations_merge,
                         left_on='brewery_id',
                         right_on='breweryId',
                         how='left').copy()

    df_full = pd.concat([df_beers, df_merged], axis=1)

    COLUMNS = ['abv', 'description', 'style_ibuMax', 'id', 'isOrganic', \
               'name', 'style_name', 'nameDisplay', 'style_fgMax', \
               'style_fgMin', 'images_icon', 'brewery_name', \
               'brewery_website', 'brewery_id', 'longitude', 'latitude']
    df_full = df_full[COLUMNS]
    df_full.drop_duplicates(inplace=True)
    df_beers = df_full
    #############
    # Transform

    # Get rid of mongo id
#    del df_beers['_id']
#    df_beers = convert_columns(df_beers)
#
#    #Subset columns on df_beers and df_breweries
#    df_beers = df_beers.loc[:, ['abv', 'description', 'style_ibuMax', 'id', 'isOrganic', 'name', 'style_name', 'nameDisplay', 'style_fgMax', 'style_fgMin']]
#    df_breweries = df_breweries.loc[:, ['images_icon', 'name', 'website', 'id']]
#
#    #Concatenate df_breweries and df_beers
#    df_beers = pd.concat([df_beers, df_breweries], axis = 1)
#    df_beers.drop_duplicates(inplace=True)

    ########
    # Save

    savefile = os.path.join(os.pardir, 'Data', 'beer_data_full.pkl')
    save_web = os.path.join(os.pardir, 'website', 'beer_data_full.pkl')


    with open(savefile, 'wb') as f:
        pickle.dump(df_beers, f, protocol=pickle.HIGHEST_PROTOCOL)
    with open(save_web, 'wb') as f:
        pickle.dump(df_beers, f, protocol=pickle.HIGHEST_PROTOCOL)
