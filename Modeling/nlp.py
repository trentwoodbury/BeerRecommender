# This file will not work unless you include the description column in the
# to_pandas_we_go.py file located in the Munging folder.
#
# The reason this file is no longer in use is that the clusters resulting
# from NMF did not add value to the classification of the beers.

import pandas as pd
import numpy as np
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
        topic_top_words = topic.argsort()[:-n_top_words - 1:-1]
        print "Topic #{}:".format(topic_idx)
        print " | ".join([feature_names[t] for t in topic_top_words])
        print '\n'

def nmf_descriptions(df):
    #INPUT: dataframe of beer info
    #OUTPUT: NMF of beer descriptions
    descs = df['style_description']
    wl = WordNetLemmatizer()

    # XXX: I believe this is an error
#    corpus = [wl.lemmatize(word) for description in descs \
#                                     for word in description.split()]

    sw = stopwords.words('english')

#    sw.extend(['hoppy', 'beer', 'like', 'typically', 'ale', 'character',
#               'estery', 'emphasized', 'medium', 'low', 'high', 'fuller',
#               'evident', 'flavor', 'alcohol', 'evident', 'perceived',
#               'style', 'variety', 'aroma', 'levels', 'body', 'color',
#               'employ', 'employed', 'derived', 'enhances', 'end',
#               'emphasis', 'element', 'either', 'duration', 'may', 'light',
#               'bodied', 'toasted', 'use', 'non', 'emerge', 'enjoyed',
#               'enhance', 'enhanced', 'content', 'cold', 'generated',
#               'absent', 'temperatures', 'temperature', 'chill',
#               'essentially', 'especially', 'level', 'type', 'used',
#               'entered', 'entry', 'enough', 'acceptable', 'brewed', 'craft'])

    tfidf = TfidfVectorizer(max_df=0.9, min_df=0.1, stop_words=sw)
    tfidf_fit = tfidf.fit_transform(descs)
    feature_names = tfidf.get_feature_names()

    nmf = NMF(n_components=10, l1_ratio = 0.5).fit(tfidf_fit)

    return nmf, feature_names


if __name__ == "__main__":
#    df = get_dataframe('../Data/beer_data_final.pkl')
    df = get_dataframe('../Data/beer_data_full.pkl')

    for col in df:
        if pd.isnull(df[col]).sum() > 5000:
            del df[col]

    df.dropna(inplace=True, axis=0)

    nmf, feature_names = nmf_descriptions(df)

    print_top_words(nmf, feature_names, 8)

    print '=' * 40
    print 'Actual Beer Names'
    print '=' * 40
    for n in df['style_shortName'].unique():
        print n


