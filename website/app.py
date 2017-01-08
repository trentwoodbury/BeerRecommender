''' Authors: Dylan Albrecht
             Trent Woodbury

    Date: December 19, 2016

    Uses bootstrap template and scikit-learn KNN model to recommend beers.

    NOTE: If we want ratings recommender, we might want GraphLab,
          or build our own factorization recommender.
'''
import os
import cPickle as pickle
from itertools import izip
from flask import Flask
from flask import render_template
from flask import request
#from flask import session
#from flask import flash
#from flask import redirect
#from flask import url_for
#from flask import g
from flask_bootstrap import Bootstrap
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import sqlite3
from utils import flatten
from utils import convert_columns
from utils import get_beer_names
from utils import get_dfs
from utils import get_dfs_train
from utils import group_by_letter
from utils import feature_select
from utils import normalize
from utils import vectorize


####################
# Global variables
####################

DATABASE = 'beer_db'

# Global data -- pd.DataFrame and gl.SFrame
DFS = None
DFS_TRAIN = None
# Template single data point, for prediction based on user input.
DFS_ONE = None

NORMALIZER = None
VECTORIZER = None

KNN = None


###########
# Web App
###########

app = Flask(__name__)

# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)


# function used for connecting to the database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/display_beer', methods=['GET', 'POST'])
def display_beer():

    global DFS_ONE
    global KNN
    global NORMALIZER
    global VECTORIZER

    if request.method == 'GET':
        beer_id = request.args.get('id')

        # Load the selected entry into DFS_ONE
        DFS_ONE = DFS[DFS['id'] == beer_id]
        del DFS_ONE['id']

        name = DFS_ONE['name'].iloc[0]
        style_name = "(" + DFS_ONE['style_name'].iloc[0] + ")"
    elif request.method == 'POST':
        # TODO: Add form validation
        text = request.form['desc']
        desc_text = unicode(text.lower())

        abv = int(request.form['abv'])

        # Load generic data point into DFS_ONE
        load_template_data_point()

        DFS_ONE['description'] = desc_text
        DFS_ONE['style_description'] = desc_text
        DFS_ONE['abv'] = abv
        DFS_ONE['style_abvMax'] = float(abv)
        DFS_ONE['style_abvMin'] = float(abv)

        name = desc_text
        style_name = " (" + unicode(abv) + "%)"
    else:
        raise ValueError("ValueError: Neither POST nor GET...")

    # Copy to local variable! (As these changes would persist)
    query_pt_pd = DFS_ONE.copy()

    query_pt_pd, _ = vectorize(query_pt_pd, vectorizer=VECTORIZER)
    query_pt_pd, _ = normalize(query_pt_pd, normalizer=NORMALIZER)

    ####################
    # Predict on point
    dist, ind = KNN.kneighbors(query_pt_pd)

    nns = DFS.iloc[ind[0]].copy()

    html = df_to_html(nns)

    return render_template('display_beer.html',
                           name=name,
                           style_name=style_name,
                           result_html=html)


def df_to_html(dfs, limit=10):
    ''' Returns block of HTML of up to 10 results
        INPUT: pd.DataFrame -- DataFrame containing nearest neighbors.
        OUTPUT: string
    '''
    html = ""

    entries = 0
    for r in dfs.iterrows():
        html += "<p>"
        html += "<h4>"
        html += unicode(entries+1) + ".  "
        html += unicode(r[1]['name'])
        html += " (" + unicode(r[1]['style_name']) + ")"
        html += "</h4>"
        html += unicode(r[1]['description'])
        html += "</p>"

        entries += 1
        if entries >= limit:
            break

    return html


def load_training_data():
    ''' Simply loads the DataFrames and does feature selection. '''
    global DFS
    global DFS_TRAIN

    DFS = get_dfs()
    DFS = feature_select(DFS)

    DFS_TRAIN = get_dfs_train()

    # Get rid of 'id' -- was used in graphlab
#    if 'id' in DFS.columns.tolist():
#        del DFS['id']
    if 'id' in DFS_TRAIN.columns.tolist():
        del DFS_TRAIN['id']


def load_model():
    global KNN
    global NORMALIZER
    global VECTORIZER

    model_file = os.path.join(os.pardir, 'Data', 'knn_model.pkl')
    with open(model_file, 'rb') as f:
        model = pickle.load(f)

    KNN = model['knn']
    NORMALIZER = model['normalizer']
    VECTORIZER = model['vectorizer']


def load_template_data_point():
    ''' Creates a global template data point 'DFS_ONE', from random sampling
        of the full training dataset.  These values will be overwritten by
        whatever the web app visitor wishes, through the form input.
    '''
    global DFS
    global DFS_ONE

    # Copy the first data point to fill in.
    DFS_ONE = DFS.iloc[0:1].copy()

    for col in DFS_ONE:
        # Fill via random sample
        DFS_ONE[col] = DFS[col].sample(1).iloc[0]

        DFS_ONE.loc[:,col] = DFS_ONE[col].astype(DFS[col].dtype)

        if DFS_ONE[col].dtype == float \
           or DFS_ONE[col].dtype == int \
           or DFS_ONE[col].dtype == bool:
            pass
        else:
            DFS_ONE[col] = ""


@app.route('/')
def main():

    beers = get_beer_names()
    beers_split = group_by_letter(beers)
    alphabet = ["#s"]
    alphabet.extend([chr(i) for i in range(65, 91)])
    index_range = range(27)

    return render_template('search_table.html',
                           result=[beers_split, alphabet, index_range])

if __name__ == '__main__':
    Bootstrap(app)

    load_training_data()
    load_template_data_point()
    load_model()

    app.run(debug=True)
