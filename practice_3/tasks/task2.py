from bs4 import BeautifulSoup
import json
import numpy


# type_li = BeautifulSoup

def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row

    site = BeautifulSoup(text, 'html.parser')
    products = site.find_all('div', attrs={"class": "product-item"})

    # Лист всех возмомжных типов списка
    types = []
    for ty in site.find_all('li'):
        types.append(ty['type'])
    types = list(set(types))
    # print(types)

    items = list()

    for product in products:
        item = dict()

        item['id'] = product.a['data-id']
        item['link'] = product.find_all('a')[1]['href']
        item['img_link'] = product.find_all('img')[0]['src']
        item['product_name'] = product.find_all('span')[0].get_text().strip()
        item['price'] = int(product.price.get_text().replace('₽', '').replace(' ', '').strip())
        item['bonus'] = int(product.strong.get_text().replace('+ начислим ', '').replace('бонусов', '').strip())

        props = product.find_all('li')
        for prop in props:
            item[prop['type']] = prop.get_text().strip()

        items.append(item)

    return items


items_list = list()

for i in range(1, 67):
    file_name_base = f'../data/data_task2/{i}.html'
    result = handle_file(file_name_base)
    items_list += result

items_list = sorted(items_list, key=lambda x: x['price'], reverse=True)

with open('../results/task2/r_task2.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(items_list, ensure_ascii=False))

filter_items = list(filter(lambda x: x['bonus'] > 2436, items_list))

with open('../results/task2/r_task2_filter.json', 'w', encoding="utf-8") as file:
    file.write(json.dumps(filter_items, ensure_ascii=False))


def statistical_characteristics():
    result_statistical = dict()
    np_items = []

    for item in items_list:
        np_items.append(item['price'])
    np_items = numpy.asarray(np_items)

    result_statistical['sum'] = numpy.sum(np_items)
    result_statistical['avr'] = result_statistical['sum'] / np_items.shape[0]
    result_statistical['max'] = np_items.max()
    result_statistical['min'] = np_items.min()

    print(result_statistical)
    return result_statistical


def tag_frequency():
    cities = []
    count_city = dict()

    for item in items_list:
        cities.append(item['product_name'].lower())

    for city in cities:
        if city in count_city:
            count_city[city] += 1
        else:
            count_city[city] = 1

    result_tag = dict(sorted(count_city.items(), key=lambda x: x[1], reverse=True))

    return result_tag


statistical_characteristics()
tag_frequency()
