import json
import sqlite3


def load_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        data_file = json.load(file)

    return data_file


def connect_to_db(db):
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    return connection


def create_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS building_subitem (
         id           INTEGER PRIMARY KEY ASC,
         id_building  INTEGER REFERENCES building (id),
         name         TEXT (255),
         place        INTEGER,
         prise        INTEGER
        )
    """)


def insert_subitem_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
           INSERT INTO building_subitem (id_building, name, place, prise)
           VALUES(
                (SELECT id FROM building WHERE name = :name),
                :name, :place, :prise
           )
       """, data)

    db.commit()


def first_query(db, name):
    cursor = db.cursor()
    res = cursor.execute(""" 
        SELECT * 
        FROM building_subitem
        WHERE id_building = (SELECT id FROM building WHERE name = ?) 
     """, [name])

    first_items = []
    for row in res.fetchall():
        item = dict(row)
        first_items.append(item)

    cursor.close()
    return first_items


def second_query(db, name):
    cursor = db.cursor()
    res = cursor.execute(""" 
           SELECT
                AVG(place) as avg_place, 
                AVG(prise) as avg_prise
           FROM building_subitem
           WHERE id_building = (SELECT id FROM building WHERE name = ?) 
        """, [name])

    items_second = []
    items_second.append(dict(res.fetchone()))

    cursor.close()
    return items_second


def third_query(db, name):
    cursor = db.cursor()
    res = cursor.execute(""" 
           SELECT *
           FROM building_subitem
           WHERE id_building = (SELECT id FROM building WHERE name = ?) 
           ORDER BY prise DESC 
        """, [name])

    items_third = []
    for row in res.fetchall():
        items_third.append(dict(row))

    cursor.close()
    return items_third


items = load_file('../data/task_2_var_05_subitem.json')
database = connect_to_db("../results/first.db")
create_table(database)

# insert_subitem_data(database, items)

first = first_query(database, 'Дортмунд 1969')
second = second_query(database, 'Гран-при ФИДЕ 1977')
third = third_query(database, 'Ставангер 1961')

with open('../results/task2/r_1.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(first, ensure_ascii=False))
with open('../results/task2/r_2.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(second, ensure_ascii=False))
with open('../results/task2/r_3.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(third, ensure_ascii=False))
