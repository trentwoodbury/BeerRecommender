import pandas as pd
import pickle
import pymongo


def get_pickle(filepath):
    #Get data from pickled file
    data = pickle.load(open(filepath))
    return data

def make_db(data):
    #Create MongoDB database called BeerDB
    #Populate database with our dictionaries from data variable
    db = client['beerDB']
    db.beer.delete_many({})
    for doc in data:
        db.beer.insert_one(doc)
    print "Original Number of Beers:", db.beer.find().count()
    return db

def get_the_good_stuff(db):
    #INPUT: full database of beers
    #Beers that have abv, description, ibu, name, and fgMax
    query1 = {'abv': {'$exists': 1}, 'description': {'$exists': 1}, 'ibu': {'$exists': 1}, 'name' : {'$exists': 1}, 'fgMax': {'$exists': 1}}
    query2 = {'abv':1, 'description': 1, 'ibu': 1, 'name': 1, 'fgMax': 1}
    full_info_beers = db.beer.find(query1, query2)
    print "Final Number of Beers:", full_info_beers.count()
    return full_info_beers

def to_pandas_we_go(cursor):
    df = pd.DataFrame(list(cursor)).loc[: , ['name', 'description', 'abv', 'fgMax', 'ibu']]
    print "Sample of Beer DataFrame \n", df.head()
    return df

def format_df(df):
    df['abv'] = pd.to_numeric(df['abv'])
    df['fgMax'] = pd.to_numeric(df['fgMax'])
    df['ibu'] = pd.to_numeric(df['ibu'])
    return df

if __name__ == "__main__":

    client = pymongo.MongoClient()

    data = get_pickle('../Data/dict_list.pkl')
    print "All {} pieces of data retrieved \n".format(len(data))

    db = make_db(data)
    full_info_beers = get_the_good_stuff(db)
    df = format_df(to_pandas_we_go(full_info_beers))
