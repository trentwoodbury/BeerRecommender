import pickle
import sqlite3

def build_database(data_base_name, beer_data):
    #INPUT: database name - should probably be "beer_db", beer_data: dataframe of beer data.
    #OUPUT: NONE. This creates the database and puts data into it.

    with sqlite3.connect(data_base_name) as connection:
        c = connection.cursor()
        try:
            c.execute("""CREATE TABLE beer_table (name TEXT, style TEXT, abv INT, finalGravity NUMERIC, ibu NUMERIC)""")
        except:
            pass

        db_size = c.execute('SELECT COUNT(name) FROM beer_table').fetchall()[0][0]

        #see if we have already put data into database
        if db_size > 0:
            c.execute('DELETE FROM beer_table')
        for row in beer_data.values:
            query = ('INSERT INTO beer_table VALUES(?,?,?,?,?)')
            c.execute(query, (row[0], row[1], row[2], row[3], row[4]))


if __name__ == "__main__":
    beer_data = pickle.load(open('../Data/beer_data_final.pkl', "r"))
    build_database("beer_db.db", beer_data)
