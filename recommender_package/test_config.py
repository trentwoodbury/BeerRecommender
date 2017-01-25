''' Authors: Dylan Albrecht
	     Trent Woodbury

    Date: January 18, 2017

    This is our particular test config file for BeerRecommender.

'''


import os

#################
# Debug setting

DEBUG_MODE = 'ON'

###################
# Database config

MONGO_USERNAME = os.environ['MONGO_USERNAME']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
MONGO_HOSTNAME = os.environ['MONGO_HOSTNAME']
MONGO_PORT = '27017'
BEER_DB = 'beer_db_test'
CRAFT_BEERS_RAW_CO = 'craft_beers_raw_test'
CRAFT_BEERS_CO = 'craft_beers_test'
# Beers Breweries Locations COllection
BBL_RAW_CO = 'bbl_raw_test'
BBL_CO = 'bbl_test'

###################
# Modeling config

# Custom column/feature selection:
COLUMNS = ['abv',
 'description',
 'style_description',
 'style_ibuMax',
 'id',
 'isOrganic',
 'name',
 'nameDisplay',
 'style_name',
 'style_fgMax',
 'style_fgMin',
 'images_icon',
 'brewery_name',
 'website']

# Configuration for model files
PROJECT_ROOT = os.path.dirname(__file__)
DATA_DIR = os.path.join(PROJECT_ROOT, os.pardir, 'tests', 'data')
DATA_FULL_PKL = 'beer_data_test_full.pkl'
DATA_TRAIN_PKL = 'beer_data_test_train.pkl'
RECOMMENDER_MODEL_PKL = 'recommender_model_test.pkl'
BEER_ID = 'id'
DROP_COLS = ['id', 'images_icon', 'website']


################
# API Settings
API_KEY = os.environ['BREWERYDB_API_KEY']

DEFAULT_BASE_URI = "http://api.brewerydb.com/v2"

#############################
# Set up our custom queries

ABV_PAGE = {4: 2} 
ABV_PAGE_QUERY_LIST = []
for k, v in ABV_PAGE.iteritems():
    a = v * [k]
    b = range(v)
    ABV_PAGE_QUERY_LIST.extend(zip(a,b))

BEER_ENDPOINT = "{}/beers?key={}".format(DEFAULT_BASE_URI, API_KEY)
BEER_ENDPOINT += "&abv={}&p={}"

BBL_ENDPOINT = "{}/beer/".format(DEFAULT_BASE_URI) + "{}"
BBL_PARAMS = {'key': API_KEY,
              'withBreweries': 'Y',
              'withIngredients': 'Y',
              'withLocations': 'Y'}
