#The purpose of this program is to convert the disparate
#.json files into a single dataframe

import yaml
import os

def get_the_data():
    dict_list = []
    counter = 0
    for filename in os.listdir('../Data'):
        if filename != '.DS_Store':
            with open('../Data/'+ str(filename)) as f:
                for everything in f:
                    count = 0
                    everything = everything.split(':')[4:-1]
                    #Remove brackets before and after dictionary
                    everything[0] = everything[0][1:]
                    everything[-1] = everything[-1][:-10]
                    new_str = ''
                    layers_deep = 0
                    for item in everything:
                        new_str += str(item) + ': '
                    new_str = new_str.replace('/', '').replace('\\', '').replace('""', '')
                    #new_str will end with ':' so let's remove that
                    new_str = new_str[:-2]
                    dict_list.append(new_str)
    return dict_list








if __name__ == "__main__":

    dict_list = get_the_data()

    # dict_list.append(yaml.load(new_str))
