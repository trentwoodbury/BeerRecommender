#The purpose of this program is to convert the disparate
#.json files into a list of dictionaries and then save these to
#a pickle file, beer_data.pkl.

import os
import pickle
import yaml


def get_the_data():
    #INPUT: None
    #OUTPUT: a list of all the data dictionaries as strings. These strings
    #need to be formatted before they can be converted to dictionaries. They
    #have all kinds of weird problems.

    dict_list = []
    for filename in os.listdir('../Data'):
        if filename != '.DS_Store':
            with open('../Data/'+ str(filename)) as f:
                for everything in f:

                    #Remove the success message at the beginning
                    #we only want the embedded dictionary with the information
                    everything = everything.split(':')[4:-1]
                    #Remove brackets before dictionary
                    everything[0] = everything[0][1:]
                    #Remove success message at end.
                    #We only want the embedded dictionary with the information
                    everything[-1] = everything[-1][:-10]

                    #Now we are going to put our results into a string
                    new_str = ''
                    for item in everything:
                        new_str += str(item) + ': '
                    new_str = new_str.replace('/', '').replace('\\', '').replace('""', '')

                    #new_str will end with ':' so let's remove that
                    #and then let's add new_str to the dict_list
                    new_str = new_str[:-2]
                    dict_list.append(new_str)
    return dict_list

def break_apart(dict_list):
    #INPUT: output of get_the_data
    #OUTPUT: a list of lists of dictionaries
    #The motivation for this is that each string in dict_list is actually multiple dictionaries. We need to split these apart so that we can evaluate them.

    #list of lists of dictionaries
    lolod = []
    for new_str in dict_list:
        temp_list = []
        split_dicts = new_str.split('}},{')
        for idx, d in enumerate(split_dicts):
            #first value in split_dicts will start with '{'
            if idx == 0:
                current_string = str(d) + '}}'
            #case where we're in the middle
            elif 0 < idx and idx < len(split_dicts)-1:
                current_string = '{' + str(d) + '}}'
            #case where we're at the last value in split_dicts
            else:
                current_string = '{' + str(d)
            temp_list.append(current_string)

        lolod.append(temp_list)
    return lolod

def try_to_dict_it(lolod):
    beer_dicts = []
    for lol in lolod:
        for d in lol:
            try:
                bd = yaml.load(d)
                beer_dicts.append(bd)
            except:
                pass

    return beer_dicts





if __name__ == "__main__":

    dict_list = get_the_data()
    lolod = break_apart(dict_list)
    beer_dicts = try_to_dict_it(lolod)
    #Save data to pickle file.
    pickle.dump(beer_dicts, open('../Data/beer_data.pkl', 'w'))
