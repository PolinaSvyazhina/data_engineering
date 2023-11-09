import json
import msgpack
import os
from statistics import mean

dataset = list()

with open('../products_5.json', 'r', encoding='utf-8') as inp:
    dataset = json.load(inp)

name_dictionary = dict()

for item in dataset:
    if item['name'] not in name_dictionary:
        name_dictionary[item['name']] = []

    name_dictionary.get(item['name']).append(item['price'])


def get_product_props(product_price_list: [int]):
    min_price = min(product_price_list)
    avg_price = mean(product_price_list)
    max_price = max(product_price_list)

    return min_price, avg_price, max_price


result_list = []

for product_name, values in name_dictionary.items():
    min_v, avg_v, max_v = get_product_props(values)
    result_list.append({
        'name': product_name,
        'min': min_v,
        'avg': avg_v,
        'max': max_v
    })

with open('../result/products_5_3_res.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps(result_list))

with open('../result/products_5_3_res.msgpack', 'wb') as out:
    out.write(msgpack.packb(result_list))

print(f"json = {os.path.getsize('../result/products_5_3_res.json')}")
print(f"msgpack = {os.path.getsize('../result/products_5_3_res.msgpack')}")

print(f"Размер JSON больше, чем MSGPACK, на {int(((os.path.getsize('../result/products_5_3_res.json')/os.path.getsize('../result/products_5_3_res.msgpack')) - 1)*100)}%")