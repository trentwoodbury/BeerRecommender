''' Authors: Trent Woodbury
             Dylan Albrecht

    Date: Deceber 16, 2016

    DESCRIPTION:

    Retrieves beer data from brewerydb and stores in MongoDB.  Multi-threaded
    and multiprocessed for speed of web-scraping.

    NOTE: Make sure you have MongoDB running.  If the collection exists, the
          script exits.

    TODO: Find out if there is a delay requirement -- is this too fast?

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
COLLECTION_NAME = 'craft_beers_raw'
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


#####################
# SCRAPING FUNCTIONS
#####################

def insert_page_json(query_url):
    ''' Takes the complete query url and inserts ONE entry into the
        MongoDB database.
        INPUT: str
        OUTPUT: None
    '''
    # TODO: 'try' statement so this doesn't fail on 'too many HTTP requests'
    query = Request(query_url)
    f = urlopen(query)
    beer_str = f.read()

    # Extract ABV and Page for printing status
    m = re.search(r'abv=\d+&p=\d+', query_url)
    abv_page, page_num = re.findall(r'\d+', m.group())

    # Insert into MongoDB
    beer_co.insert_one(json.loads(beer_str))

    pn = "Entry: ABV {0} PAGE {1}"
    process_name = pn.format(abv_page, page_num)
    print process_name + " ... Done"

#    XXX: Doesn't seem to (fully) work yet -- Gives Thread Exception:
#    XXX: 'module' object has no attribute 'get_ident'
#    tpn = "Thread {0} ABV {1} PAGE {2}"
#    thread_process_name = tpn.format(threading.get_ident(), abv_page,
#                                     page_num)
#    print thread_process_name + " ... Done"


def insert_pages_json_threaded(query_url, pages):
    ''' Takes incomplete string query url -- has 'p={}'.  Iterates over
        pages and adds one thread per page -- 'p={0}', 'p={1}' ...
        INPUT: str, number
        OUTPUT: None
    '''
#    # How to limit the threads to threads of two:
#    evn_pages = [i for i in range(pages) if i % 2 == 0]
#    odd_pages = [i+1 for i in range(pages) if i % 2 == 1]
#
#    # Control number of threads created:
#    for (start, end) in zip(evn_pages, odd_pages):

    threads = []

    # Add one thread per page:
    for page_num in range(pages):
        str_arg = query_url.format(page_num)
        threads.append(threading.Thread(target=insert_page_json,
                                        args=([str_arg])))

    for th in threads:
        th.start()

    for th in threads:
        th.join()


def get_beer(abv_pages):
    ''' Retrieves craft beers stored in brewerydb API and pushes the results
        into a MongoDB database 'beer_db', collection 'craft_beers'.
        Adds one 'abv' threaded process per processor.
        INPUT: Pages dictionary
        OUTPUT: None
    '''
    query_url = 'http://api.brewerydb.com/v2/beers?key={}&abv={}&p={}'

    pool = mp.Pool(processes=mp.cpu_count())

    # Add one multi-threaded process for each ABV
    multi_proc = [pool.apply_async(insert_pages_json_threaded,
                                   (query_url.format(api_key, abv, "{}"),
                                    pages,)) \
                  for abv, pages in abv_pages.iteritems()]

    for proc in multi_proc:
        proc.get()

    print "Done Retrieving Beers!"


if __name__ == "__main__":
    BreweryDb.configure(api_key)

    # Chosen data to pull:
    abv_pages = {4: 16, 5: 67, 6: 54, 7: 39, 8: 30, 9: 22, 10: 19}
    #abv_pages = {4: 16}

    get_beer(abv_pages)
