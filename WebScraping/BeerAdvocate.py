from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd


def get_beer():
    #Gets beer data from beeradvocate.com
    all_beer_info = []

    driver = webdriver.Chrome()
    driver.get("https://www.beeradvocate.com/beer/")
    assert "Beer" in driver.title
    beer_name = driver.find_element_by_id('ba-content')
    beer_info = (beer_name.text).split('\n')[2:-1]
    all_beer_info.extend(beer_info)

    #Go on to next pages
    for i in range(13):
        # https://www.beeradvocate.com/beer/?start=25
        link = driver.find_element_by_link_text('next')
        link.click()
        beer_name = driver.find_element_by_id('ba-content')
        beer_info = (beer_name.text).split('\n')[2:-1]
        all_beer_info.extend(beer_info)

    driver.close()
    return all_beer_info

def parse_it_up(beer_info):
    #INPUT: beer info, list of beer information from beer advocate
    #OUPUT: formatted list of beer information. This is a list where
    #all of the beers are separated into sublists
    formatted_beer = []
    last_index = 0

    #look for the star, indicating that we're
    for current_index, element in enumerate(beer_info):
        if unichr(9733) in element:
                formatted_beer.append(beer_info[last_index:current_index+1])
                last_index = current_index + 1

    return formatted_beer

def dataframe_time(formatted_beer):
    #INPUT: formatted_beer_list, output from parse_it_up()
    #OUPUT: a formatted dataframe of our data
    df = pd.DataFrame(formatted_beer[1:]).iloc[:, 2:10]
    df.drop(df.columns[3], axis=1, inplace = True)
    df.drop(df.columns[-2], axis=1, inplace = True)

    #Let's name these preliminary columns
    df.columns = ['Name', 'Brewer', 'Style/ABV', 'Ratings', 'More Ratings', 'Review']
    return df

def abv_style(df):
    #Let's get the ABV and Beer Type columns
    style = []
    abv = []
    style_abv = df['Style/ABV']
    for row in style_abv:
        row_list = row.split(' / ')
        if 'ABV' in row_list[-1]:
            #Often times there are multiple styles. We are only concerned
            #With the primary style
            style.append(row_list[0])
            abv.append(row_list[-1].split('%')[0])
        #There are some empty ABV fields. We will set the to 5%.
        else:
            style.append(row_list[0])
            abv.append('5')

    df.drop(['Style/ABV'], axis = 1, inplace = True, errors = 'ignore')
    df['Style'] = style
    df['ABV'] = abv
    return df

def fix_ratings(df):
    #Now we have the Style and ABV fields. Let's get the ratings section formatted. We are only concerned with the average rating, so we will extract that.
    ratings = []
    for row in df['Ratings']:
        first_split = row.split('|')
        second_split = first_split[-1].split(': ')
        ratings.append(float(second_split[-1]))
    df['Ratings'] = ratings
    return df

def smell_feel(df):
    #INPUT: df output of fix_ratings
    #OUTPUT: same df with 'More Ratings' columns replaced with a smell and a feel column

    the_smells = []
    the_feels = []
    for row in df['More Ratings']:
        smell, feel = row.split(' | ')[1], row.split(' | ')[3]
        smell = float(smell.split(': ')[1])
        feel = float(feel.split(': ')[1])
        the_smells.append(smell)
        the_feels.append(feel)

    df.drop(['More Ratings'], axis = 1, inplace = True, errors = 'ignore')
    df['Smell'] = the_smells
    df['Feel'] = the_feels
    return df


if __name__ == "__main__":
    beer_info = get_beer()
    formatted_beer = parse_it_up(beer_info)
    print formatted_beer
    df = dataframe_time(formatted_beer)
    df = abv_style(df)
    df = fix_ratings(df)
    df = smell_feel(df)
    df.to_csv('beers.csv')
