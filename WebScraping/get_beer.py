from brewerydb import *


if __name__ == "__main__":
    BreweryDb.configure(api_key)

    #we are going to get a json object from the beer database called beers
    beers = BreweryDb.beers({'abv':"4,10"})

    print beers
