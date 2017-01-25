''' Authors: Dylan Albrecht
             Trent Woodbury

    Date: January 25, 2017

    Script that uses the recommender_package to pull data from BreweryDB
    and put it in a MongoDB.

    Also transforms the data MongoDB raw collection -> MongoDB clean
    collection.

'''
import sys

# Local package context
from package_context import recommender_package

from recommender_package.api.etl import DataETL
from recommender_package.munging.process import NDLReducer
from recommender_package.database.collection import CollectionManager
from recommender_package.config import BEER_DB
from recommender_package.config import CRAFT_BEERS_RAW_CO
from recommender_package.config import CRAFT_BEERS_CO
from recommender_package.config import BBL_RAW_CO
from recommender_package.config import BBL_CO
from recommender_package.config import API_KEY
from recommender_package.config import ABV_PAGE_QUERY_LIST
from recommender_package.config import BEER_ENDPOINT
from recommender_package.config import BBL_ENDPOINT
from recommender_package.config import BBL_PARAMS



if __name__ == "__main__":
    ##
    # Populate the beers raw collection:
    dbm = CollectionManager(database_name=BEER_DB,
                            collection_name=CRAFT_BEERS_RAW_CO)
    beer_raw_co = dbm.connect()

    if beer_raw_co:
        if beer_raw_co.count():
            print "Collection {!r} populated".format(CRAFT_BEERS_RAW_CO)
        else:
            etl = DataETL(BEER_ENDPOINT, {}, ABV_PAGE_QUERY_LIST, beer_raw_co)
            etl.run_sequential()
    else:
        print "Collection {!r} None!".format(CRAFT_BEERS_RAW_CO)

    ##
    # Populate the beers clean collection:
    beer_co = dbm.connect(CRAFT_BEERS_CO)

    if beer_co:
        if beer_co.count():
            print "Collection {!r} populated".format(CRAFT_BEERS_CO)
        else:
            ndl_reducer = NDLReducer()
            for entry in beer_raw_co.find():
                for e in entry['data']:
                    new_entries = ndl_reducer.transform(e)
                    for ne in new_entries:
                        beer_co.insert_one(ne)
    else:
        print "Collection {!r} None!".format(CRAFT_BEERS_CO)

    ##
    # Populate the bbl raw collection:
    bbl_raw_co = dbm.connect(BBL_RAW_CO)

    if bbl_raw_co:
        if bbl_raw_co.count():
            print "Collection {!r} populated".format(BBL_RAW_CO)
        else:
            # List of ids -- query_list
            beer_ids_list = list(beer_co.find({"id": {"$exists": "true"}},
                                              {"id": 1, "_id": 0}))
            query_list = [id.values() for id in beer_ids_list]

            etl_bbl = DataETL(BBL_ENDPOINT, BBL_PARAMS, query_list, bbl_raw_co)
            etl_bbl.run_sequential()
    else:
        print "Collection {!r} None!".format(BBL_RAW_CO)

    ##
    # Populate the bbl clean collection:

    bbl_co = dbm.connect(BBL_CO)

    if bbl_co:
        if bbl_co.count():
            print "Collection {!r} populated".format(BBL_CO)
        else:
            ndl_reducer = NDLReducer(form_unique_id=['id', 'breweries_id',
                                                     'breweries_locations_id'])
            for entry in bbl_raw_co.find():
                if entry['status'] == 'failure':
                    continue

                new_entries = ndl_reducer.transform(entry['data'])
                for ne in new_entries:
                    bbl_co.insert_one(ne)
    else:
        print "Collection {!r} None!".format(BBL_CO)


