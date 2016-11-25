def format_json(filepath):
    #INPUT: filepath to json file to be fixed up
    #OUTPUT: a list of python dictionaries in string format

    with open(filepath) as fp:
        for line in fp:
            b_string = line.replace('\\', '')

    #now lets break the dictionary up into a list of dictionaries
    layers_deep = 0
    dict_list = []
    for idx, char in enumerate(b_string):
        if char == "{":
            start_idx = idx
            layers_deep +=1
        elif char == "}":
            layers_deep -=1
            if layers_deep == 0:
                dict_list.append(b_string[start_idx: idx+1])
    return dict_list


def eval_doc(doc_item):
    #INPUT: string representation of a dictionary with some issues
    #OUTPUT: string with issues resolved
    layers_deep = 0
    output = ''
    inquotes = False
    for idx, char in enumerate(doc_item):
        if char == '{' and idx > 0:
            layers_deep +=1
        elif char == '}' and idx < len(doc_item)-1 and layers_deep == 0:
            continue
        elif char == '}':
            layers_deep -=1
        elif char == '"' and not inquotes:
            inquotes = True
        elif char == '"':
            if doc_item[idx+1] == ":" or doc_item[idx+1] == "," or doc_item[idx+1] == "}":
                inquotes = False
            else:
                continue

        output += doc_item[idx]

    return output
