import pymongo
import pickle

def get_pickle(filepath):
    data = pickle.load(open(filepath))
    return data


if __name__ == "__main__":
    data = get_pickle('../Data/dict_list.pkl')
    print "All {} pieces of data retrieved".format(len(data))
    print data[210]
