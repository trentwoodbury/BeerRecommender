''' Authors: Dylan Albrecht
	     Trent Woodbury

    Date: January 18, 2017

    This is our particular config file for BeerRecommender.  If you are setting
    up your own beer recommender based on the package code, you might want
    to change some of these settings.

    The idea is that the code will work just fine -- you don't really need
    to change other package source files -- when you make changes to
    this config file.

'''


import os

#################
# Debug setting

try:
    DEBUG_MODE = os.environ['BEER_RECOMMENDER_DEBUG']
except KeyError as e:
    s = "Try setting environment variable {}='ON' to turn on DEBUG_MODE"
    print s.format('BEER_RECOMMENDER_DEBUG')
    print e
    DEBUG_MODE = 'OFF'

###################
# Database config

try:
    MONGO_USERNAME = os.environ['MONGO_USERNAME']
    MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
    MONGO_HOSTNAME = os.environ['MONGO_HOSTNAME']
except KeyError as e:
    s = "Try setting environment variables {}, {}, {}"
    print s.format('MONGO_USERNAME', 'MONGO_PASSWORD', 'MONGO_HOSTNAME')
    print e
    MONGO_USERNAME = ""
    MONGO_PASSWORD = ""
    MONGO_HOSTNAME = 'localhost'

MONGO_PORT = '27017'
BEER_DB = 'beer_db'
CRAFT_BEERS_RAW_CO = 'craft_beers_raw'
CRAFT_BEERS_CO = 'craft_beers'
BBL_RAW_CO = 'bbl_raw'
BBL_CO = 'bbl'

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
DATA_DIR = os.path.join(PROJECT_ROOT, os.pardir, 'Data')
DATA_FULL_PKL = 'beer_data_full.pkl'
DATA_TRAIN_PKL = 'beer_data_train.pkl'
RECOMMENDER_MODEL_PKL = 'recommender_model.pkl'
BEER_ID = 'id'
DROP_COLS = ['id', 'images_icon', 'website']


################
# API Settings
API_KEY = os.environ['BREWERYDB_API_KEY']

DEFAULT_BASE_URI = "http://api.brewerydb.com/v2"

# BreweryDb:
SIMPLE_ENDPOINTS = ["beers", "breweries", "categories", "events",
                    "featured", "features", "fluidsizes", "glassware",
                    "locations", "guilds", "heartbeat", "ingredients",
                    "search", "search/upc", "socialsites", "styles"]
SINGLE_PARAM_ENDPOINTS = ["beer", "brewery", "category", "event",
                          "feature", "glass", "guild", "ingredient",
                          "location", "socialsite", "style", "menu"]

#############################
# Set up our custom queries

ABV_PAGE = {4: 16, 5: 67, 6: 54, 7: 39, 8: 30, 9: 22, 10: 19}
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
