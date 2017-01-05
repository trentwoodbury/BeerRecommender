# BeerRecommender
A Recommendation System for Craft Beers

# Status
This project is currently in progress. We are currently deploying and editing the website at beerecommender.com.

# Usage Guide
First, contact Trent or Dylan about getting the API access codes. All of the following filepaths will be relative to the parent directory for this github project. If you have cloned this project, that folder will be called BeerRecommender.

Once you have the access codes, you can pull the data by running WebScraping/get_beer_fast.py. Either one will work. These files will put fill out the Mongo database with the relavent beers.

From here run Munging/raw_to_clean_db.py. This will clean up the mongo Database that you have created. At this point make sure you have a "Data" folder in your BeerRecommender folder. Then run Munging/mongo_to_df.py. Munging/mongo_to_df.py will save the mongo database as a .pkl file in the Data and website folders.

Finally run website/app.py. This will start a local version of the website. Open up your browser and you will be able to see the website at the url: http://localhost:5000/

## Coded Using<br>
AWS<br>
CSS<br>
Flask<br>
HTML <br>
MongoDB<br>
Pandas<br>
Python<br>
SKlearn<br>
SQLite<br>


The BreweryDB API
