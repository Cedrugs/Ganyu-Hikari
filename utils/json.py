"""
JSON tools that copied from MenuDocs
"""

import json


__all__ = ('read_json', 'write_json', 'jsonify')


def read_json(path, encoding=None) -> dict:
    """
    A function used to get data from json
    Params:
     - path (str) : Path of the json file.
    Return:
    - Dictionary of the json data.
    """
    with open(path, encoding=encoding) as file:
        data = json.load(file)
    return data


def write_json(data, filepath):
    """
    A function used to write data to a json file
    Params:
     - data (dict) : The data to write to the file
     - filename (string) : The name of the file to write to
    """
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


def jsonify(**kwargs):
    """
    A function used to convert kwargs to dictionary
    Params:
     - kwargs (str) : Kwargs for the json
    Return:
    - Dictionary of the kwargs
    """
    if kwargs:
        return kwargs
