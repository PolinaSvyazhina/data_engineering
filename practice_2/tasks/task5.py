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

allowed_name_list = ['name',
                     'status',
                     'in_production',
                     'original_language',
                     'popularity',
                     'number_of_episodes',
                     'vote_average',
                     'vote_count',
                     ]

resulting_dict = {}

dataset = []

with open('../tvs.json', 'r', encoding='utf-8') as inp:
    dataset = json.load(inp)

for item in dataset:
    for key in item.keys():
        if key not in allowed_name_list:
            continue
        if key not in resulting_dict:
            resulting_dict[key] = {} if isinstance(item[key], str) or isinstance(item[key], bool) else []
        if isinstance(item[key], str) or isinstance(item[key], bool):
            if item[key] not in resulting_dict[key]:
                resulting_dict[key][item[key]] = 0
            resulting_dict[key][item[key]] += 1
        else:
            resulting_dict[key].append(item[key])


def resolve_strategy(data, metric_name):
    if isinstance(data, dict):
        return process_str(data, metric_name)
    if isinstance(data, list):
        return process_numeric(data, metric_name)

    raise


def process_str(dict: {}, name: str):
    return {
        name: json.dumps(dict)
    }


def process_numeric(data_list: [], name: str):
    filtered_list = list(filter(lambda x: x is not None, data_list))
    mapped_list = list(map(lambda x: float(x), filtered_list))

    return {
        name: {
            'avg': mean(mapped_list),
            'min': min(mapped_list),
            'max': max(mapped_list),
            'sum': sum(mapped_list),
            'std_err': stats.sem(mapped_list)
        }
    }


result = list(map(lambda x: resolve_strategy(resulting_dict[x], x), list(resulting_dict.keys())))

with open('../result/task5/task5_r.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps(result))

with open('../result/task5/task5_r.msgpack', 'wb') as out:
    out.write(msgpack.packb(dataset))

df = pd.DataFrame([x for x in dataset])

with open('../result/task5/task5_r.csv', 'w', encoding='utf-8') as out:
    out.write(df.to_csv(index=False))

df.to_pickle('../task5_r.pkl')
