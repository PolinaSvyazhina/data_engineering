import csv
import msgpack
import sqlite3
import json

def read_msgpack(file_name):
    with open(file_name, 'rb') as file:
        data_file = msgpack.load(file)

        for item in data_file:
            if len(item) == 6:
                item['category'] = 'no'
            item['version'] = 0
    return data_file


def read_update_data(file_name):
    items = []

    with open(file_name, newline='\n', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        reader.__next__()
        for row in reader:
            if len(row) == 0: continue
            item = dict()
            item['name'] = row[0]
            item['method'] = row[1]
            if item['method'] == 'available':
                item['param'] = row[2] == "True"
            elif item['method'] != 'remove':
                item['param'] = float(row[2])
            items.append(item)

    return items


def connect_to_db(db):
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    return connection


def create_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
         id           INTEGER PRIMARY KEY ASC,
         name         TEXT (255),
         price        REAL,
         quantity     INTEGER,
         category     TEXT(255),
         fromCity     TEXT(255),
         isAvailable  TEXT(255),
         views        INTEGER,
         version      INTEGER
        )
    """)


def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO product (name, price, quantity, category, fromCity, isAvailable, views, version)
        VALUES(
            :name, :price, :quantity, :category,
            :fromCity, :isAvailable, :views, :version
        )
    """, data)

    db.commit()


def delete_by_name(db, name):
    cursor = db.cursor()
    cursor.execute(" DELETE FROM product WHERE name = ? ", [name])
    db.commit()


def update_price_by_percent(db, name, percent):
    cursor = db.cursor()
    cursor.execute(" UPDATE product SET price = ROUND(price * (1 + ?), 2) WHERE name = ? ", [percent, name])
    cursor.execute(" UPDATE product SET version = version + 1  WHERE name = ? ", [name])
    db.commit()


def update_price(db, name, param):
    cursor = db.cursor()
    res = cursor.execute("""
     UPDATE product SET price = (price + ?) WHERE (name = ?) AND ((price + ?) > 0)
     """, [param, name, param])

    if res.rowcount > 0:
        cursor.execute(" UPDATE product SET version = version + 1  WHERE name = ? ", [name])
        db.commit()


def update_quantity(db, name, param):
    cursor = db.cursor()
    res = cursor.execute("UPDATE product SET quantity = (quantity + ?) WHERE (name = ?) AND ((quantity + ?) > 0)",
                         [param, name, param])
    if res.rowcount > 0:
        cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
        db.commit()


def update_available(db, name, param):
    cursor = db.cursor()
    cursor.execute("UPDATE product SET isAvailable = ? WHERE name = ?  ", [param, name])
    cursor.execute(" UPDATE product SET version = version + 1  WHERE name = ? ", [name])
    db.commit()


def handle_update(db, update_items):
    for item in update_items:
        match item['method']:
            case 'remove':
                pass
                # delete_by_name(db, item['name'])
            case 'price_percent':
                print(f"update_price_by_percent {item['name']}")
                update_price_by_percent(db, item['name'], item['param'])
            case 'price_abs':
                print(f"price_abs {item['name']}")
                update_price(db, item['name'], item['param'])
            case 'quantity_sub':
                print(f"quantity_sub {item['name']}")
                update_quantity(db, item['name'], item['param'])
            case 'quantity_add':
                print(f"quantity_add {item['name']}")
                update_quantity(db, item['name'], item['param'])
            case 'available':
                print(f"available {item['name']}")
                update_available(db, item['name'], item['param'])


def top_update_product(db):
    items_list = []

    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM product ORDER BY version DESC LIMIT 10")

    for row in res.fetchall():
        items_list.append(dict(row))
    cursor.close()

    return items_list


def statistical_characteristics_by_price(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT 
        category,
        MIN(price) as min,
        MAX(price) as max,
        AVG(price) as avg,
        SUM(price) as sum
        FROM product
        GROUP BY category
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()

    return items


def statistical_characteristics_by_quantity(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT 
        category,
        MIN(quantity) as min,
        MAX(quantity) as max,
        AVG(quantity) as avg,
        SUM(quantity) as sum
        FROM product
        GROUP BY category
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()

    return items


def get_top_by_views(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT *
        FROM product
        WHERE views > 60000
        ORDER BY views DESC
    """)

    items_list = []

    for row in res.fetchall():
        items_list.append(dict(row))
    cursor.close()

    return items_list


data_msgpack = read_msgpack('../data/task_4_var_05_product_data.msgpack')
data_update = read_update_data('../data/task_4_var_05_update_data.csv')
database = connect_to_db("../results/fourth.db")
create_table(database)
# insert_data(database, data_msgpack)
# handle_update(database, data_update)

top_update = top_update_product(database)
st_by_price = statistical_characteristics_by_price(database)
st_quantity = statistical_characteristics_by_quantity(database)
top = get_top_by_views(database)

with open('../results/task4/st_by_price.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(st_by_price, ensure_ascii=False))

with open('../results/task4/st_quantity.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(st_quantity, ensure_ascii=False))

with open('../results/task4/top.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(top, ensure_ascii=False))