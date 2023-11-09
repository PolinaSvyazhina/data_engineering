import json
import pickle


def update_price(product, price_info):
    method = price_info['method']
    match method:
        case "add":
            product['price'] = product['price'] + price_info['param']
        case "sub":
            product['price'] = product['price'] - price_info['param']
        case "percent+":
            product['price'] = product['price'] * (1 + price_info["param"])
        case "percent-":
            product['price'] = product['price'] * (1 - price_info["param"])

    product["price"] = round(product["price"], 2)

with open("../price_info_5.json") as file:
    price_info = json.load(file)

with open("../products_5.pkl", "rb") as file:
    products = pickle.load(file)

price_product_info = {}

for item in price_info:
    price_product_info[item['name']] = item
for product in products:
    current_product = price_product_info[product['name']]
    update_price(product, current_product)

with open('../result/update_price_products.pkl', 'wb') as result:
    result.write(pickle.dumps(products))