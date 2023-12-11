import json
import pickle
import sqlite3


def parse_data(file_name):
    with open(file_name, "rb") as file:
        data_file = pickle.load(file)
    return data_file


def connect_to_database(database):
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    return connection


def create_table(db):
    cursor = db.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS building (
            id           INTEGER    PRIMARY KEY ASC,
            name         TEXT (255),
            city         TEXT (100),
            begin        TEXT (100),
            system       TEXT (100),
            tours_count  INTEGER,
            min_rating   INTEGER,
            time_on_game INTEGER
            )""")
    db.commit()


def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO building (name, city, begin, system, tours_count, min_rating, time_on_game)
        VALUES(
            :name, :city, :begin, :system,
            :tours_count, :min_rating, :time_on_game
        )
    """, data)

    db.commit()


def get_top_by_tours_count(db):
    cursor = db.cursor()

    res = cursor.execute(
        "SELECT * FROM building ORDER BY time_on_game DESC LIMIT 15")
    res = res.fetchall()

    items_list = []

    for row in res:
        items_list.append(dict(row))
    cursor.close()

    return items_list


def get_top_by_min_rating(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT * 
        FROM building 
        WHERE min_rating > 2400
        ORDER BY time_on_game DESC LIMIT 15
        """)

    res = res.fetchall()

    items_list = []

    for row in res:
        items_list.append(dict(row))
    cursor.close()

    return items_list


def statistical_characteristics(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT 
        MIN(time_on_game) as min,
        MAX(time_on_game) as max,
        AVG(time_on_game) as avg,
        SUM(time_on_game) as sum
        FROM building
    """)

    items_st = []
    res = res.fetchone()
    items_st.append(dict(res))
    cursor.close()

    return items_st

items = parse_data('../data/task_1_var_05_item.pkl')


def tag_frequency(db):
    cursor = db.cursor()

    result_tag = cursor.execute("""
                    SELECT
                        CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM building) as count,
                        city
                    FROM building
                    GROUP BY city
                
    """)
    items_tag = []
    for row in result_tag.fetchall():
        items_tag.append(dict(row))
    cursor.close()
    return items_tag


db = connect_to_database("../results/first.db")
create_table(db)
# insert_data(db, items)

st = statistical_characteristics(db)
tag = tag_frequency(db)

res_1 = get_top_by_tours_count(db)
res_2 = get_top_by_min_rating(db)

with open('../results/task1/r_task1.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(res_1, ensure_ascii=False))

with open('../results/task1/r_task1_filter.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(res_2, ensure_ascii=False))

with open('../results/task1/r_statistical.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(st, ensure_ascii=False))

with open('../results/task1/r_tag.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(tag, ensure_ascii=False))
