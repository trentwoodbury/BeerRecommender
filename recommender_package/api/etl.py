import requests
import multiprocessing as mp
import threading

from ..config import DEFAULT_BASE_URI
from ..config import SIMPLE_ENDPOINTS
from ..config import SINGLE_PARAM_ENDPOINTS


COLLECTION = None


class DataETL(object):
    ''' This class takes a substitution query endpoint, a parameter dictionary,
        an iterable list (one item per query), and a pyMongo collection:
        
        Schematic example:
            end_point = "http://api.brewerydb.com/v2/beer/{}"
            params = {'key': API_KEY}
            query_list = ['abc123', 'def456', ...] # beer ids
            collection = pymongo.database['beer_co']

        NOTE: It's a little trickier when iterating over parameters -- need
              to set up the end_point correctly, pass params={}, and the
              query_list with each entry being a list of parameters.  There
              is an example in ..utils.config.BEERS_ENDPOINT
    '''

    def __init__(self, end_point, params, query_list, collection):
        '''
            INPUT: string, dict, iterable, pyMongo collection
            OUPUT: None
        '''
        self._check_collection(collection)

        self.set_global_collection(collection)
        self.url_endpoint = end_point
        self.params = params

        # This is a list of a list of parameters that are iterated over,
        # and substituted into the url_endpoint
        # -- self.url_endpoint.format(*query_list[0])
        self.query_list = query_list


    def _check_collection(self, collection):
        if collection:
            if collection.count():
                print "Warning: Nonempty collection"
        else:
            raise ValueError("Collection is None!")


    def set_global_collection(self, collection):
        ''' We want a global collection for multiprocessing/threading. '''
        global COLLECTION
        COLLECTION = collection


    def run_sequential(self):
        for query_one in self.query_list:
            insert_one(self.url_endpoint, self.params, query_one)


    def run_parallel(self):
        ps = [mp.Process(target=insert_one,
                         args=(self.url_endpoint, self.params, query_one,)) \
              for query_one in self.query_list]

        for p in ps:
            p.start()
        for p in ps:
            p.join()


    def run_threaded(self, query_list):
        threads = []

        for query_one in self.query_list:
            threads.append(threading.Thread(target=insert_one,
                                            args=([query_one])))

        for th in threads:
            th.start()
        for th in threads:
            th.join()


def insert_one(endpoint, params, query_one):
    ''' We need a non-instance method for pickling, for multiprocessing/
        threading.

        TODO: Add error handling -- request, json, insert_one
    '''
    global COLLECTION

    query_url = endpoint.format(*query_one)

    req = requests.get(query_url, params=params)

    # Insert into MongoDB collection
    COLLECTION.insert_one(req.json())

