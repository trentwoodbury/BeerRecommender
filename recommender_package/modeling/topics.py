# This file will not work unless you include the description column in the
# to_pandas_we_go.py file located in the Munging folder.
#
# The reason this file is no longer in use is that the clusters resulting
# from NMF did not add value to the classification of the beers.
import os
import sys
import cPickle as pickle
from string import punctuation
from unidecode import unidecode
import unicodedata

import pandas as pd
import numpy as np
import pattern.en as en
#from nltk.corpus import stopwords
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import NMF
from sklearn.metrics import silhouette_score
from bokeh.plotting import figure
from bokeh.plotting import show
from bokeh.plotting import output_file
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource
from bokeh.palettes import mpl

from recommender_package.utils.modeling import get_dfs_train
from recommender_package.utils.munging import raw_to_transform_data


# Load these once globally
PARSER = None
#STOP_WORDS = set(stopwords.words('english') + list(ENGLISH_STOP_WORDS))
STOP_WORDS = set(list(ENGLISH_STOP_WORDS))
PUNCT_TBL = dict.fromkeys(i for i in xrange(sys.maxunicode)
                        if unicodedata.category(unichr(i)).startswith('P'))


def print_top_words(model_components, feature_names, n_top_words=5):
    for topic_idx, topic in enumerate(model_components):
        topic_top_words = topic.argsort()[:-n_top_words - 1:-1]
        print "Topic #{}:".format(topic_idx)
        print " | ".join([feature_names[t] for t in topic_top_words])
        print '\n'


def tokenizer(doc):
    ''' Custom tokenizer.
        INPUT: string (one document)
        OUTPUT: list (of tokens)
    '''

    # Replace '-' with ' ', and remove all other punctuation:
    doc = doc.translate({45: u' '})
    sdoc = unidecode(doc)
    sdoc = sdoc.lower().translate(None, punctuation)

    ldoc = [en.lemma(w) for w in sdoc.split() if w not in STOP_WORDS]

    return ldoc


def topic_plot(W, H, feature_names, dfs, offline=False):
    n_topics = len(H)

    df_plot = dfs[['style_name']].copy()
    df_plot['topic'] = np.argmax(W, axis=1)
    dfg_plot = df_plot[['style_name', 'topic']].groupby('style_name').median()

    dfg_plot['topic'] = dfg_plot['topic'].apply(lambda x: int(x))

    dfg_plot.sort_values('topic', inplace=True)
    dfg_plot.reset_index(inplace=True)
    names = dfg_plot['style_name'].values
    words = feature_names

    Nx = H.shape[1]
    Ny = len(dfg_plot)

    colormap = mpl['Plasma'][n_topics]
    xname, yname, color, alpha, topic = [], [], [], [], []
    for i, row in dfg_plot.iterrows():
        #counts[:,i] = H[row['topic'], :]
        alpha += (H[row['topic'], :] / np.max(H[row['topic'], :])).tolist()
        color += [colormap[row['topic']]] * Nx

        for w in words:
            xname.append(w)
            yname.append(row['style_name'])
            topic.append(row['topic'])

    source = ColumnDataSource(data=dict(
        xname=xname,
        yname=yname,
        colors=color,
        alphas=alpha,
        topic=topic,
    ))

    p = figure(title="Beer Topics by Color",
               x_axis_location="above",
               tools="hover,save,wheel_zoom,pan,reset",
               x_range=list(words), y_range=list(names))

    p.plot_width = 600
    p.plot_height = 600
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "6pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = np.pi/3

    p.rect('xname', 'yname', 0.9, 0.9, source=source,
           color='colors', alpha='alphas', line_color=None,
           hover_line_color='black', hover_color='colors')

    p.select_one(HoverTool).tooltips = [
        ('names', '@yname, @xname'),
        ('topic', '@topic'),
    ]

    if offline:
        output_file("topics_plot.html", title="Beer Topic Modeling")
        show(p)

    return p, source


def nmf(X, n_topics=5):
    nmf = NMF(n_components=n_topics)

    # X = W * H  --  (beers x topics) * (topics x words)
    W = nmf.fit_transform(X)
    H = nmf.components_

    return W, H


def topic_silhouettes(X, topic_range=range(2,10)):
    s = []
    for t in topic_range:
        nmf = NMF(n_components=t)

        # X = W * H  --  (beers x topics) * (topics x words)
        W = nmf.fit_transform(X)
        H = nmf.components_

        topics = np.argmax(W, axis=1)
        s.append(silhouette_score(X, topics))

    return s


def topic_silhouettes_plot(silhouette_scores, n_topics, offline=False):
    source = ColumnDataSource(data=dict(x=n_topics, y=silhouette_scores))

    p = figure()
    p.scatter('x', 'y', source=source)

    if offline:
        output_file("topic_silhouettes.html", title="Beer Topic Modeling")
        show(p)

    return p


if __name__ == "__main__":
    dfs = get_dfs_train()
    dfs = raw_to_transform_data(dfs)
    dfs['full_description'] = dfs['description'] + ' ' \
                              + dfs['style_description']

    descs = dfs['full_description']
    vec = CountVectorizer(max_df=0.9, min_df=0.1, tokenizer=tokenizer,
                          stop_words=STOP_WORDS)
    tfidf = TfidfTransformer()
    X = tfidf.fit_transform(vec.fit_transform(descs))
    W, H = nmf(X)
    p = topic_plot(W, H, feature_names, dfs)
    output_file("beer_topics.html", title="Beer Topic Modeling")
    show(p)
