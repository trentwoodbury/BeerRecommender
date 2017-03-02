''' Authors: Dylan Albrecht
             Trent Woodbury

    Date: December 18, 2016

    Some useful functions for working with data.

'''

import os
import cPickle as pickle
import os

from .munging import raw_to_transform_data
from .modeling import get_dfs
from ..config import DATA_DIR
from ..config import DATA_FULL_PKL

def first_letter(cell):
    return str(cell[0]).lower()

def get_beer_names():
    #makes sorted list of all the beers
    beer_df = get_dfs()
    beer_df = raw_to_transform_data(beer_df)
    beer_df.sort_values('name', inplace=True)
    beer_df.reset_index(inplace=True)
    names_and_ids = beer_df[['name', 'id', 'breweries_name']]
    return names_and_ids.values


def group_by_letter(names):
    alphabet = range(97, 123)
    groups = [[] for i in range(27)]
    for name in names:
        letter = ord(name[0][0].lower())
        if letter in range(97, 123):
            groups[122 - letter].append(name)
        else:
            groups[-1].append(name)
    return groups
