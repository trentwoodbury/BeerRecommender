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

if __name__ == "__main__":

    client = pymongo.MongoClient()

    data = get_pickle('../Data/dict_list.pkl')
    print "All {} pieces of data retrieved".format(len(data))
    print data[210]

    make_db(data)
