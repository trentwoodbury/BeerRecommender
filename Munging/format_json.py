#The purpose of this program is to convert the disparate
#.json files into a single dataframe
import yaml




if __name__ == "__main__":

    #dict_list will be a list with all of the dictionaries in it
    dict_list = []
    #dict_as_string should be a list of dictionaries read as strings
    for item in dict_as_string:
        dict_list.append(yaml.load(eval_doc(item)))
