#This file will not work unless you include the description column in the to_pandas_we_go.py file located in the Munging folder.
#The reason this file is no longer in use is that the clusters resulting from NMF did not add value to the classification of the beers.

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer


def get_dataframe(filepath):
    #Load data
    data = pickle.load(open(filepath))
    return data

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print "Topic #{}:".format(topic_idx)
        print " | ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        print '\n'

def nmf_descriptions(df):
    #INPUT: dataframe of beer info
    #OUTPUT: NMF of beer descriptions
    descs = df['description']
    wl = WordNetLemmatizer()
    corpus = [wl.lemmatize(word) for description in descs for word in description.split()]

    sw = stopwords.words('english')
    sw.extend(['hoppy', 'beer', 'like', 'typically', 'ale', 'character', 'estery', 'emphasized', 'medium', 'low', 'high', 'fuller', 'evident', 'flavor', 'alcohol', 'evident', 'perceived', 'style', 'variety', 'aroma', 'levels', 'body', 'color', 'employ', 'employed', 'derived', 'enhances', 'end', 'emphasis', 'element', 'either', 'duration', 'may', 'light', 'bodied', 'toasted', 'use', 'non', 'emerge', 'enjoyed', 'enhance', 'enhanced', 'content', 'cold', 'generated', 'absent', 'temperatures', 'temperature', 'chill', 'essentially', 'especially', 'level', 'type', 'used', 'entered', 'entry', 'enough', 'acceptable'])
    tfidf = TfidfVectorizer(max_df = .9, stop_words = sw)
    tfidf_fit = tfidf.fit_transform(corpus)
    feature_names = tfidf.get_feature_names()

    nmf = NMF(n_components = 2, l1_ratio = 0.5).fit(tfidf_fit)

    return nmf, feature_names


if __name__ == "__main__":
    df = get_dataframe('../Data/beer_data_final.pkl')
    nmf, feature_names = nmf_descriptions(df)
    print_top_words(nmf, feature_names, 5 )
