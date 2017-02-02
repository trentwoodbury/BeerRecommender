''' Authors: Dylan Albrecht
             Trent Woodbury

    Date: January 25, 2017

    Script that uses the recommender_package to pull data from BreweryDB
    and put it in a MongoDB.

    Also transforms the data MongoDB raw collection -> MongoDB clean
    collection.

'''
import sys

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


def populated(collection):
    if collection:
        if collection.count():
#            raise ValueError("Collection {!r} populated".format(
#                             collection.name))
            return True
        else:
            return False
    else:
        raise ValueError("Collection {!r} None!".format(collection.name))


if __name__ == "__main__":
    ##
    # Populate the beers raw collection:
    dbm = CollectionManager(database_name=BEER_DB,
                            collection_name=CRAFT_BEERS_RAW_CO)
    beer_raw_co = dbm.connect()

    if not populated(beer_raw_co):
        etl = DataETL(BEER_ENDPOINT, {}, ABV_PAGE_QUERY_LIST, beer_raw_co)
        etl.run_sequential()

    ##
    # Populate the beers clean collection:
    beer_co = dbm.connect(CRAFT_BEERS_CO)

    if not populated(beer_co):
        ndl_reducer = NDLReducer()
        for entry in beer_raw_co.find():
            for e in entry['data']:
                new_entries = ndl_reducer.transform(e)
                for ne in new_entries:
                    beer_co.insert_one(ne)

    ##
    # Populate the bbl raw collection:
    bbl_raw_co = dbm.connect(BBL_RAW_CO)

    if not populated(bbl_raw_co):
        # List of ids -- query_list
        beer_ids_list = list(beer_co.find({"id": {"$exists": "true"}},
                                          {"id": 1, "_id": 0}))
        query_list = [id.values() for id in beer_ids_list]

        etl_bbl = DataETL(BBL_ENDPOINT, BBL_PARAMS, query_list, bbl_raw_co)
        etl_bbl.run_sequential()

    ##
    # Populate the bbl clean collection:

    bbl_co = dbm.connect(BBL_CO)

    if not populated(bbl_co):
        ndl_reducer = NDLReducer(form_unique_id=['id', 'breweries_id',
                                                 'breweries_locations_id'])
        for entry in bbl_raw_co.find():
            if entry['status'] == 'failure':
                continue

            new_entries = ndl_reducer.transform(entry['data'])
            for ne in new_entries:
                bbl_co.insert_one(ne)


