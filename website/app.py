from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3

DATABASE = 'beer_db'
app = Flask(__name__)

# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

# function used for connecting to the database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
