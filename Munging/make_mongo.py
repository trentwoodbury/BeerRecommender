import pymongo
import pickle

def get_pickle(filepath):
    #Get data from pickled file
    data = pickle.load(open(filepath))
    return data

def make_db(data):
    #Create MongoDB database called BeerDB
    #Populate database with our dictionaries from data variable
    db = client['beerDB']
    for doc in data:
        db.beer.insert(doc)
    print db.beer.find().count()
    return db

def get_the_good_stuff(db):
    query1 = {'abv': {'$exists': 1}, 'description': {'$exists': 1}, 'ibu': {'$exists': 1}, 'name' : {'$exists': 1}, 'fgMax': {'$exists': 1}}
    query2 = {'abv':1, 'description': 1, 'ibu': 1, 'name': 1, 'fgMax': 1}
    full_info_beers = db.beer.find(query1, query2)
    print full_info_beers.count()
    return full_info_beers

if __name__ == "__main__":

    client = pymongo.MongoClient()

    data = get_pickle('../Data/dict_list.pkl')
    print "All {} pieces of data retrieved".format(len(data))
    print data[210]

    db = make_db(data)
    full_info_beers = get_the_good_stuff(db)
