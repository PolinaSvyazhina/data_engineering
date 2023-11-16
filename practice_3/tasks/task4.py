import json
import os
from statistics import mean
import xmltodict
import codecs
import numpy as np

file_list = os.listdir('../data/data_task4')

result_list = []

for file in file_list:
    with codecs.open(f'../data/data_task4/{file}', 'r', encoding='cp1251') as f:
        data = xmltodict.parse(f.read())

        clothing_list = data['clothing-items']['clothing']

        for cloth in clothing_list:
            result_list.append(cloth)

result_list.sort(key=lambda v: v['category'], reverse=True)

with codecs.open('../results/task4/r_task4.json', 'w', encoding='cp1251') as out:
    out.write(json.dumps(result_list, ensure_ascii=False))

filter_list = list(filter(lambda x: float(x['rating']) > 3.5, result_list))

with codecs.open('../results/task4/r_task4_fil.json', 'w', encoding='cp1251') as out:
    out.write(json.dumps(filter_list, ensure_ascii=False))

static = list(map(lambda x: float(x['price']), result_list))

static_json = {
    'avg': mean(static),
    'min': min(static),
    'max': max(static),
    'sum': sum(static),
    'std': np.std(static)
}

with codecs.open('../results/task4/4_3_result.json', 'w', encoding='cp1251') as out:
    out.write(json.dumps(static_json, ensure_ascii=False))

tag_dict = {}

for item in result_list:
    name_list = item['name'].split(' ')
    for token in name_list:
        if token not in tag_dict:
            tag_dict[token] = 0
        tag_dict[token] += 1

with codecs.open('../results/task4/4_4_result.json', 'w', encoding='cp1251') as out:
    out.write(json.dumps(tag_dict, ensure_ascii=False))

