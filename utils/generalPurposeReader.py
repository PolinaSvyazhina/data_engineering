import csv
import json
import re
import msgpack
import pandas as pd


def get_object_list(path: str):
    format = path.split('.')[-1]

    data_list = []

    match format:
        case 'csv':
            data_list = csv_strategy(path)
        case 'json':
            data_list = json_strategy(path)
        case 'msgpack':
            data_list = msgpack_strategy(path)
        case 'text':
            data_list = text_strategy(path)

    return data_list


def json_strategy(w):
    with open(w, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return list(data)


def csv_strategy(w):
    with open(w, 'r', newline='', encoding='utf-8') as file:
        df = pd.read_csv(w, delimiter=';')
        data = df.to_dict(orient='records')
    return data


def msgpack_strategy(w):
    with open(w, 'rb') as file:
        data = msgpack.unpack(file)
    return data


def text_strategy(w):
    with open(w, 'r', encoding='utf-8') as file:
        text = file.read()

    objects = text.split('=====')
    regex = r'(\w+)::((?:\d+|\w+))'
    pattern = re.compile(regex)


    result = []
    for o in objects:
        matches = re.findall(pattern, o)
        for match in matches:
            data = {}
            (key, value) = match
            data[key] = int(value) if value.isdigit() else value
            result.append(data)

    return result
