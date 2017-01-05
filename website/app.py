from flask import Flask, render_template, request, session, flash, redirect, url_for, g
from flask_bootstrap import Bootstrap
import pandas as pd
import sqlite3

def get_beer_names():
    beer_df =  pd.read_pickle("beer_data_final.pkl")
    return list(beer_df['name'])

DATABASE = 'beer_db'
app = Flask(__name__)

# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

# function used for connecting to the database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def main():

    beers = get_beer_names()
    beers_split = []

    #Make a list of lists so that we have 5 beers per row
    for i in range(len(beers)):
        if i % 5 == 0:
            beers_split.append([])
        if len(beers[i]) > 22:
            beers_split[-1].append(str(beers[i][:19]) + '...')
        else:
            beers_split[-1].append(beers[i])


    #ensure That our table ends with 5 columns
    if len(beers_split[-1]) != 5:
        beers_split = beers_split[:-1]

    return render_template('names_table.html', result=beers_split)

if __name__ == '__main__':
    Bootstrap(app)
    app.run(debug=True)
