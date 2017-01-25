''' Authors: Dylan Albrecht
             Trent Woodbury

    Data: January 24, 2017

    DESCRIPTION:

    This class is intended to process a nested API entry, and return
    a list of flattened entries, possibly adding a unique id based on
    joining specified fields.  The reason to do this is to take
    
    {beer:id, breweries:[{locations:[{long:#1}, ...]},
                         {locations:[{long:#2}, ...]}, ...]}

    to a list of flattened dictionaries:

    [{beer:id, berweries_locations_long:#1, ..., unique_id: beer_brew_loc_id},
        .               .               .
        .               .               .
     {beer:id, berweries_locations_long:#2, ..., unique_id: beer_brew_loc_id},
        .               .               .
        .               .               .
     ]

    EXAMPLE:
    
        entry = {'a': 1, 'b': [{'d': ['1', '2']}], 'c': '1'}
        ndl_reducer = NDLReducer(form_unique_id=['b_d', 'c'])
        ndl_reducer.transform(entry)
        [{'a': 1, 'b_d': '1', 'c': '1', 'unique_id': '1_1'},
         {'a': 1, 'b_d': '2', 'c': '1', 'unique_id': '2_1'}]


    TODO: This class could be made more general -- it only deals with
          nested dictionaries with two level nested lists.  For example,
          by making a better recursive algorithm.
'''

from ..utils.munging import flatten

class NDLReducer(object):
    def __init__(self, form_unique_id=[]):
        self.form_unique_id = form_unique_id


    def list_add(self, list_dictionaries):
        items = []

        for d in list_dictionaries:
            for k, v in d.items():
                if isinstance(v, list):
                    d_tmp = d.copy()
                    
                    for val in v:
                        d_tmp[k] = val
                        items.append(d_tmp.copy())

                    break

        if not items:
            return [d]
        else:
            return items

    def transform(self, entry):
        flattened_entry = flatten(entry)

        dict_list = []
        for d in self.list_add([flattened_entry]):
            dict_list.append(flatten(d))

        flat_dict_list = []
        for dl in self.list_add(dict_list):
            flat_dict_list.append(flatten(dl))

        # Add unique identifier:
        if self.form_unique_id:
            for fd in flat_dict_list:
                uid = []
                for i in self.form_unique_id:
                    try:
                        uid.append(fd[i])
                    except KeyError as e:
                        print e

                fd['unique_id'] = '_'.join(uid)

        return flat_dict_list


