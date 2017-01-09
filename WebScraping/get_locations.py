''' Authors: Trent Woodbury
             Dylan Albrecht

    Date: January 8th, 2017

    DESCRIPTION: Retrieves location data for each location and stores in MongoDB as locations_raw.

    and multiprocessed for speed of web-scraping.

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
COLLECTION_NAME = 'locations_raw'
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


def insert_location_json():
    ''' Takes the beer_id and inserts ONE entry into the Mongo database.
        INPUT: str
        OUTPUT: None
    '''

    #loop through each beer in the MongoDB craft_beers collection
    page_nums = range(1,188)
    for page_num in page_nums:
        query_url = 'http://api.brewerydb.com/v2/locations?key={}&p={}'.format(api_key, page_num)
        query = Request(query_url)
        f = urlopen(query)
        brewery_str = f.read()

        # Insert into MongoDB
        beer_co.insert_one(json.loads(brewery_str))

if __name__ == "__main__":
    #Takes roughly 5 minutes to run
    insert_location_json()
