import sys

import recommender_package.web_scraping.get_breweries as gb
from recommender_package.api.etl import DataETL
from recommender_package.database import CollectionManager
from recommender_package.config import API_KEY
from recommender_package.config import ABV_PAGE_QUERY_LIST
from recommender_package.config import ABV_PAGE_TEST_QUERY_LIST
from recommender_package.config import BEERS_ENDPOINT
from recommender_package.config import BEERID_ENDPOINT
from recommender_package.config import BEERID_PARAMS



if __name__ == "__main__":
    ##
    # Populate the beers collection:
    dbm = CollectionManager(collection_name='beer_test')
    beer_co = dbm.connect()

    if beer_co:
        if beer_co.count():
            print "Collection already populated!"
        else:
#            etl = DataETL(BEERS_ENDPOINT, {}, ABV_PAGE_QUERY_LIST, beer_co)
            etl = DataETL(BEERS_ENDPOINT, {}, ABV_PAGE_TEST_QUERY_LIST, beer_co)
            etl.run_parallel()
    else:
        print 

    ##
    # Populate the breweries collection:
#    breweries_co = dbm.connect(BREWERIES_CO)
    breweries_co = dbm.connect('breweries_test')

    # List of ids
    beer_ids = gb.get_beer_id_list()
    beer_ids_test = beer_ids[:10]

    if breweries_co:
        if breweries_co.count():
            print "Collection already populated!"
        else:
            etl_breweries = DataETL(BEERID_ENDPOINT, BEERID_PARAMS,
                                    beer_ids_test, breweries_co)
            etl_breweries.run_parallel()

