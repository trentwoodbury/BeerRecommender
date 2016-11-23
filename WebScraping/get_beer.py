from brewerydb import *
import json


def get_beer(start_page, qty):
    #input: start page of query, how many pages to query
    #output: json of beers
    beers = []
    for i in range(start_page, start_page+qty):
        beers.append(BreweryDb.beers({'page' : i, 'abv': "4,10"}))
    return beers


def store_beer(outfile):
    #input: outfile, filepath to where resultant json will be stored
    #output: saves json file.
    with open(outfile, 'w') as outfile:
        for beer_dict in beer_list:
            json.dump(beer_dict, outfile)

if __name__ == "__main__":
    BreweryDb.configure(api_key)

    beer_list = get_beer(1, 399)

    store_beer('../Data/beerdb.json')
