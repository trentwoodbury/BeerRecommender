''' Authors: Dylan Albrecht
             Trent Woodbury

    Date: December 18, 2016

    Some useful functions for working with data.

'''

import os

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from .config import MONGO_USERNAME
from .config import MONGO_PASSWORD
from .config import MONGO_HOSTNAME
from .config import MONGO_PORT
from .config import BEER_DB
from .config import CRAFT_BEERS_CO
from .config import BREWERIES_CO
from .config import LOCATIONS_CO


class CollectionManager(object):
    def __init__(self, database_name=BEER_DB, collection_name=CRAFT_BEERS_CO,
                       offline=False):
        self.__name__ = 'CollectionManager'
        self.database = None
        self.collection = None
        self.database_name = database_name
        self.collection_name = collection_name
        self.offline=offline

        if offline:
            self.hostname = 'localhost'
        else:
            self.hostname = MONGO_HOSTNAME

        self.username = MONGO_USERNAME
        self.password = MONGO_PASSWORD
        self.port = MONGO_PORT


    def __repr__(self):
        s_fmt = "{0}(database_name={1!r}, collection_name={2!r}, offline={3})"
        s = s_fmt.format(self.__name__, self.database_name,
                         self.collection_name, self.offline)

        return s


    def __str__(self):
        if self.collection:
            s = ("=================================================\n"
                 "Connected to MongoDB {0}:{1}\n"
                 "Database: {2}\n"
                 "Collection: {3}\n"
                )
            s = s.format(self.hostname, self.port, self.database_name,
                         self.collection_name)
        else:
            s = ("=================================================\n"
                 "Not connected to MongoDB"
                )

        return s

    def connect(self, collection_name=None):
        ''' Script to connect to the 'beer_db' MongoDB database, as set up in
            the environment variables.
            INPUT: None
            OUTPUT: Mongo Collection -- 'craft_beers'
        '''
        if collection_name:
            self.collection_name=collection_name

        if not self.database:
            address = 'mongodb://'
            address += self.username + ':'
            address += self.password + '@'
            address += self.hostname

            # Check server:
            try:
                cli = MongoClient(address, serverSelectionTimeoutMS=100)
            except ConnectionFailure as e:
                print "Server error!  (Is it plugged in?): "
                print e
                raise e

            self.database = cli[self.database_name]

            if not self.database:
                raise ValueError('Database is None')

        self.collection = self.database[self.collection_name]

        if not self.collection:
            raise ValueError('Collection is None')

        return self.collection

