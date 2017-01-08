''' Authors: Trent Woodbury
             Dylan Albrecht

    Date: January 8th, 2017

    DESCRIPTION: Retrieves brewery data for each beer and attaches brewery data to dictionary associated with each beer.

    and multiprocessed for speed of web-scraping.

    NOTE: Make sure you have MongoDB running.
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

def mongo_connect():
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
    return beerdb


if __name__ == "__main__":
    beerdb = mongo_connect()
