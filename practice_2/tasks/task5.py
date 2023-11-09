import json
from statistics import mean
from scipy import stats
import msgpack
import pandas as pd

# Работаем с полями
# name: str
# status: str
# in_production: str
# original_language: str
# popularity: float
# number_of_episodes: int
# vote_average: float
# vote_count: float

name_dict = {}
status_dict = {}
in_production_dict = {}
number_of_episodes_list = []
original_language_dict = {}
popularity_list = []
vote_avg_list = []
vote_count_list = []

dataset = []

with open('../tvs.json', 'r', encoding='utf-8') as inp:
    dataset = json.load(inp)

for item in dataset:
    if item['name'] not in name_dict:
        name_dict[item['name']] = 0

    name_dict[item['name']] += 1

    if item['status'] not in status_dict:
        status_dict[item['status']] = 0

    status_dict[item['status']] += 1

    if item['in_production'] not in in_production_dict:
        in_production_dict[item['in_production']] = 0

    in_production_dict[item['in_production']] += 1

    if item['original_language'] not in original_language_dict:
        original_language_dict[item['original_language']] = 0

    original_language_dict[item['original_language']] += 1

    number_of_episodes_list.append(item['number_of_episodes'])
    popularity_list.append(item['popularity'])
    vote_avg_list.append(item['vote_average'])
    vote_count_list.append(item['vote_count'])

number_of_episodes_list = list(filter(lambda x: x is not None, number_of_episodes_list))
popularity_list = list(filter(lambda x: x is not None, popularity_list))
vote_avg_list = list(filter(lambda x: x is not None, vote_avg_list))
vote_count_list = list(filter(lambda x: x is not None, vote_count_list))

result = []

result.append({
    'name': json.dumps(name_dict),
    'status': json.dumps(status_dict),
    'in_production': json.dumps(in_production_dict),
    'original_language': json.dumps(original_language_dict),
    'number_of_episodes': {
        'avg': mean(number_of_episodes_list),
        'min': min(number_of_episodes_list),
        'max': max(number_of_episodes_list),
        'sum': sum(number_of_episodes_list),
        'std_err': stats.sem(number_of_episodes_list)
    },
    'popularity': {
        'avg': mean(popularity_list),
        'min': min(popularity_list),
        'max': max(popularity_list),
        'sum': sum(popularity_list),
        'std_err': stats.sem(popularity_list)
    },
    'vote_average': {
        'avg': mean(vote_avg_list),
        'min': min(vote_avg_list),
        'max': max(vote_avg_list),
        'sum': sum(vote_avg_list),
        'std_err': stats.sem(vote_avg_list)
    },
    'vote_count': {
        'avg': mean(vote_count_list),
        'min': min(vote_count_list),
        'max': max(vote_count_list),
        'sum': sum(vote_count_list),
        'std_err': stats.sem(vote_count_list)
    },
})

with open('../result/task5_r.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps(result))

with open('../result/task5_r.msgpack', 'wb') as out:
    out.write(msgpack.packb(result))

df = pd.DataFrame([x for x in result])

with open('../result/task5_r.csv', 'w', encoding='utf-8') as out:
    out.write(df.to_csv(index=False))

df.to_pickle('../result/task5_r.pkl')



