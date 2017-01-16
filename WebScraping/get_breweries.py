''' Authors: Trent Woodbury
             Dylan Albrecht

    Date: January 8th, 2017

    DESCRIPTION: Retrieves brewery data for each beer and attaches brewery data to dictionary associated with each beer.

    NOTE: Make sure you have MongoDB running. To run AWS MongoDB locally, use mongo $MONGO_HOSTNAME:27017 -u $MONGO_USERNAME -p $MONGO_PASSWORD --authenticationDatabase admin
'''

import sys
import os
import re
import multiprocessing as mp
import threading

import json
from urllib2 import Request, urlopen, URLError
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from brewerydb import *
from api_key import api_key

#####################
# GLOBAL MONGO SETUP
#####################

DB_NAME = 'beer_db'
COLLECTION_NAME = 'breweries_raw'
MONGO_USERNAME = os.environ['MONGO_USERNAME']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
MONGO_HOSTNAME = os.environ['MONGO_HOSTNAME']

try:
    address = 'mongodb://'
    address += MONGO_USERNAME + ':'
    address += MONGO_PASSWORD + '@'
    address += MONGO_HOSTNAME
    dbconn = MongoClient(address, serverSelectionTimeoutMS=10)
    dbconn.server_info()

except ServerSelectionTimeoutError as e:
    print "Server error!  (Is it plugged in?): "
    print e
    raise e

beerdb = dbconn[DB_NAME]

# Name of MongoDB collection
cols = beerdb.collection_names()

if COLLECTION_NAME in cols:
    print COLLECTION_NAME + ' already exists! '
    sys.exit()
    # Drop and start over? Or do nothing?
    #beerco = beerdb[COLLECTION_NAME]
    #beerco.drop()

# Global Craft Beer Collection:
beer_co = beerdb[COLLECTION_NAME]

##########################################

def get_beer_id_list():
    #INPUT: none
    #OUTPUT: list of beer ids from Mongo Database

    #loop through each beer in the MongoDB craft_beers collection
    beer_ids_list = list(beerdb.craft_beers.find({"id":{"$exists": "true"}}, {"id":1, "_id":0}))
    beer_ids = [id.values() for id in beer_ids_list]
    return beer_ids


def insert_brewery_json(beer_id):
    ''' Takes the beer_id and inserts ONE entry into the Mongo database.
        INPUT: beer_ids, output of get_beer_id_list
        OUTPUT: None
    '''
    for beer_id in beer_ids:
        query_url = 'http://api.brewerydb.com/v2/beer/{}/breweries?key={}?withLocations=Y'.format(beer_id[0],api_key)
        query = Request(query_url)
        f = urlopen(query)
        brewery_str = f.read()

        # Insert into MongoDB
        beer_co.insert_one(json.loads(brewery_str))

def multi_import(beer_ids):
    #INPUT: beer_ids, list of beer ids
    #OUPUT: None

    p = mp.Pool(mp.cpu_count())
    p.map(insert_brewery_json, beer_ids)



if __name__ == "__main__":
    #This takes ~45 minutes to run
    beer_ids = get_beer_id_list()
    multi_import(beer_ids)
