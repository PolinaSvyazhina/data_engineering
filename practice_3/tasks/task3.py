import json
import os
from statistics import mean
import xmltodict
import codecs
import numpy as np

file_list = os.listdir('../data/data_task3')

result_list = []

for i in file_list:
    with open(f'../data/data_task3/{i}', 'r',encoding='cp1251') as f:
        # result_list.append(xmltodict.parse(f.read()))
        data = xmltodict.parse(f.read())

        star_list = data['star']
        result_list.append(star_list)

result_list = sorted(result_list, key = lambda x: x['name'], reverse=True)
with open('../results/task3/r_task3.json', 'w', encoding='cp1251') as out:
    out.write(json.dumps(result_list,  ensure_ascii=False))

filter_result = list(filter(lambda x: float(x['radius']) > 343547708, result_list))

with open('../results/task3/r_task3_filter.json', 'w', encoding='cp1251') as out:
    out.write(json.dumps(filter_result,  ensure_ascii=False))

static = list(map(lambda x: float(x['radius']), result_list))

static_json = {
    'avg': mean(static),
    'min': min(static),
    'max': max(static),
    'sum': sum(static),
    'std': np.std(static)
}

tag_dict = {}

for item in result_list:
    name_list = item['constellation'].split(' ')
    for token in name_list:
        if token not in tag_dict:
            tag_dict[token] = 0
        tag_dict[token] += 1

