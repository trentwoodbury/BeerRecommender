import pandas as pd
import pickle
import pymongo


def get_pickle(filepath):
    #Get data from pickled file
    data = pickle.load(open(filepath))
    subsetted_data = []
    for d in data:
        try:
            d_subset = {'name' : d['name'], 'description': d['style']['description'],
            'abv': d['abv'], 'ibu': d['ibu'], 'finalGravity': d['style']['fgMax']}
            subsetted_data.append(d_subset)
        except:
            pass
    return subsetted_data

def to_pandas_we_go(data):
    df = pd.DataFrame(data).loc[: , ['name', 'description', 'abv', 'finalGravity', 'ibu']]
    print "Sample of Beer DataFrame \n", df.head(), '\n\n'
    return df

def format_df(df):
    df['abv'] = pd.to_numeric(df['abv'])
    df['finalGravity'] = pd.to_numeric(df['finalGravity'])
    df['ibu'] = pd.to_numeric(df['ibu'])
    return df.drop_duplicates()

if __name__ == "__main__":

    client = pymongo.MongoClient()

    data = get_pickle('../Data/beer_data.pkl')
    df = format_df(to_pandas_we_go(data))

    pickle.dump(df, open('../Data/beer_data_final.pkl', 'w'))
    print "All {} pieces of data retrieved \n".format(df.shape[0])
