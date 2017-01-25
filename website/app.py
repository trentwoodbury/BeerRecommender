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

import pandas as pd
from sklearn.neighbors import NearestNeighbors
from flask import Flask
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap

# Add local package context for importing:
from package_context import recommender_package

from recommender_package.utils.munging import raw_to_transform_data
from recommender_package.utils.modeling import get_dfs
from recommender_package.utils.website import get_beer_names
from recommender_package.utils.website import group_by_letter
from recommender_package.config import DATA_DIR
from recommender_package.config import RECOMMENDER_MODEL_PKL
from recommender_package.config import DEBUG_MODE


####################
# Global variables
####################

# Global data -- pd.DataFrame
DFS_BEER_ID = None
# Template single data point, for prediction based on user input.
DFS_ONE = None

TRANSFORMER = None
RECOMMMENDER = None

###########
# Web App
###########

application = app = Flask(__name__)

@app.route('/display_beer', methods=['GET', 'POST'])
def display_beer():

    global DFS_BEER_ID
    global DFS_ONE
    global RECOMMENDER
    global TRANSFORMER

    if request.method == 'GET':
        beer_id = request.args.get('id')
        DFS_ONE = DFS_BEER_ID.loc[[beer_id]].copy()

        name = DFS_ONE['name'].iloc[0]
        brewery = DFS_ONE['brewery_name'].iloc[0]
        style_name = "(" + DFS_ONE['style_name'].iloc[0] + ")"
    elif request.method == 'POST':
        # TODO: Add form validation
        text = request.form['desc']
        desc_text = unicode(text.lower())
        abv = int(request.form['abv'])

        # Load generic data point into DFS_ONE
        load_template_data_point()

        # XXX: make sure the columns are in our selected columns!
        DFS_ONE['description'] = desc_text
        DFS_ONE['abv'] = abv

        name = desc_text
        style_name = " (" + unicode(abv) + "%)"
        brewery = ""
    else:
        raise ValueError("ValueError: Neither POST nor GET...")

    results = predict_results()

    return render_template('display_beer.html',
                           name=name,
                           style_name=style_name,
                           brewery=brewery,
                           results=results)


def predict_results():
    global DFS_BEER_ID
    global DFS_ONE
    global TRANSFORMER
    global RECOMMENDER

    ####################
    # Predict on point
    dfs_one = DFS_ONE.copy()
    dfs_one = TRANSFORMER.transform(dfs_one)
    indices = RECOMMENDER.predict(dfs_one)

    nns = DFS_BEER_ID.loc[indices].copy()

    beer_names = []
    beer_style_names = []
    beer_brewery_names = []
    beer_descriptions = []
    for r in nns.iterrows():
        beer_names.append(r[1]['name'])
        beer_style_names.append(r[1]['style_name'])
        beer_brewery_names.append(r[1]['brewery_name'])

        if r[1]['description']:
            beer_descriptions.append(r[1]['description'])
        else:
            beer_descriptions.append(r[1]['style_description'])

    results = zip(beer_names, beer_style_names, beer_brewery_names,
                 beer_descriptions)

    return results


def load_model():
    global DFS_BEER_ID
    global RECOMMENDER
    global TRANSFORMER

    DFS_BEER_ID = get_dfs()
    DFS_BEER_ID = raw_to_transform_data(DFS_BEER_ID)

    model_file = os.path.join(DATA_DIR, RECOMMENDER_MODEL_PKL)
    with open(model_file, 'rb') as f:
        model = pickle.load(f)

    RECOMMENDER = model['recommender']
    TRANSFORMER = model['transformer']


def load_template_data_point():
    ''' Creates a global template data point 'DFS_ONE', from random sampling
        of the full training dataset.  These values will be overwritten by
        whatever the web app visitor wishes, through the form input.
    '''
    global DFS_BEER_ID
    global DFS_ONE

    # Copy the first data point to fill in.
    DFS_ONE = DFS_BEER_ID.iloc[0:1].copy()

    for col in DFS_ONE:
        # Fill via random sample
        DFS_ONE[col] = DFS_BEER_ID[col].sample(1).iloc[0]

        DFS_ONE.loc[:,col] = DFS_ONE[col].astype(DFS_BEER_ID[col].dtype)

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


def load_data_model():
    Bootstrap(app)

    load_model()
    load_template_data_point()


def run():
    if DEBUG_MODE == 'ON':
        app.run(debug=True)
    else:
        app.run()

########################################################
# Load on startup (for elasticbeanstalk, when imported)
load_data_model()


if __name__ == '__main__':
    run()
