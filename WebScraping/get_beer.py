from brewerydb import *
from api_key import api_key
import json
from urllib2 import Request, urlopen, URLError

def get_beer_url(url_req):
    request = Request(url_req)

    try:
    	response = urlopen(request)
    	beers = response.read()
        return beers
    except URLError, e:
        print 'Got an error code:', e



def get_beer():
    #input: start page of query, how many pages to query
    #output: json of beers
    abv_pages = {4: 16, 5: 67, 6: 54, 7: 39, 8: 30, 9: 22, 10: 19}
    beers = []
    for abv in abv_pages:
        for page_num in range(abv_pages[abv]):
            query = Request('http://api.brewerydb.com/v2/beers?key={}&abv={}&p={}'.format(api_key, abv, page_num))
            f = urlopen(query)
            beer = f.read()
            beers.append(f.read())
            filepath = '../Data/abv_'+str(abv)+'_page_'+str(page_num) + '.json'
            with open(filepath, 'w') as output:
                output.write("{}".format(beer))
    return beers


if __name__ == "__main__":
    BreweryDb.configure(api_key)

    beer_list = get_beer()
