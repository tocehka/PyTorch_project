import json

from nlp import allowed_lexeme_list

DELIMETER = "^"
DELETE_GROUP = ["Категория", "images_path"]

def max_length_index(arr):
    max_val = 0
    index = 0
    for i in range(0, len(arr)):
        if len(arr[i]) >= max_val:
            max_val = len(arr[i])
            index = i
    return max_val, index

def parsed_list_to_dict(arr, index=False):
    dictd = {}
    for field in arr:
        dictd[field.split(DELIMETER)[0]] = field.split(DELIMETER)[1]
    if index != False:
        dictd["index"] = index
    return dictd

def dict_to_json(dictd, index=False):
    if not isinstance(index, int) and index == False:
        return json.dumps(dictd, ensure_ascii=False)
    return {"data":json.dumps(dictd, ensure_ascii=False), "index":index}


def create_indexed_nlp_dict(arr, index):
    listd = []
    for field in arr:
        if field.split(DELIMETER)[0] in DELETE_GROUP:
            continue
        listd.append(field.split(DELIMETER)[0].lower())
        listd.append(field.split(DELIMETER)[1].lower())
    return {"set":allowed_lexeme_list(listd), "index":index}
    

