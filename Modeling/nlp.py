# This file will not work unless you include the description column in the
# to_pandas_we_go.py file located in the Munging folder.
#
# The reason this file is no longer in use is that the clusters resulting
# from NMF did not add value to the classification of the beers.
import sys
import cPickle as pickle
from string import punctuation
import unicodedata

import pandas as pd
import numpy as np
from spacy.en import English
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF


def get_dataframe(filepath):
    #Load data
    data = pickle.load(open(filepath))
    return data

def print_top_words(model_components, feature_names, n_top_words=5):
    for topic_idx, topic in enumerate(model_components):
        topic_top_words = topic.argsort()[:-n_top_words - 1:-1]
        print "Topic #{}:".format(topic_idx)
        print " | ".join([feature_names[t] for t in topic_top_words])
        print '\n'

def tokenizer(doc):
    # Replace '-' with ' ', and remove all other punctuation:
    doc = doc.translate({45: u' '})
    doc = doc.translate(PUNCT_TBL)

    # SpaCy for lemmatization, parsing, parts of speech
    sdoc = PARSER(doc)

    stop_pos = set(['PUNCT', 'NUM', 'X', 'SPACE'])

    ldoc = [s.lemma_.lower() for s in sdoc if (s.pos not in stop_pos)]

    return ldoc


def nmf_descriptions(df):
    #INPUT: dataframe of beer info
    #OUTPUT: NMF of beer descriptions
    descs = df['full_description']
#    wl = WordNetLemmatizer()
#
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
#    tfidf = TfidfVectorizer(max_df=0.9, min_df=0.1, tokenizer=tokenizer,
#                            stop_words=STOP_WORDS)
#    tfidf_fit = tfidf.fit_transform(descs)

    vec = CountVectorizer(max_df=0.9, min_df=0.1, tokenizer=tokenizer,
                          stop_words=STOP_WORDS)
    tfidf = TfidfTransformer()
    nmf = NMF(n_components=5, l1_ratio=0.5)

    pipe = Pipeline([('vec', vec), ('tfidf', tfidf), ('nmf', nmf)])

    pipe.fit(descs)

    model_components = pipe.named_steps['nmf'].components_
    feature_names = pipe.named_steps['vec'].get_feature_names()

    return model_components, feature_names


if __name__ == "__main__":
    PARSER = English()
    STOP_WORDS = set(stopwords.words('english') + list(ENGLISH_STOP_WORDS))
    PUNCT_TBL = dict.fromkeys(i for i in xrange(sys.maxunicode)
                            if unicodedata.category(unichr(i)).startswith('P'))

#    df = get_dataframe('../Data/beer_data_final.pkl')
    df = get_dataframe('../Data/beer_data_full.pkl')

    for col in df:
        if pd.isnull(df[col]).sum() > 5000:
            del df[col]

    df.dropna(inplace=True, axis=0)

    df['full_description'] = df['description'] + ' ' + df['style_description']

    model_components, feature_names = nmf_descriptions(df)

    print_top_words(model_components, feature_names, n_top_words=8)

#    print '=' * 40
#    print 'Actual Beer Names'
#    print '=' * 40
#    for n in df['style_shortName'].unique():
#        print n


