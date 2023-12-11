import pymongo

from utils.generalPurposeReader import get_object_list
from utils.jsonDumper import json_dump

client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db = client.test_database
collection = db.example_collection

collection.insert_many(get_object_list('../data/task_2_item.json'))

json_dump(list(collection.aggregate([
        {"$group": {"_id": None, "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
    ])), '../results/task2/t2_1_result')
json_dump(list(collection.aggregate([
        {"$group": {"_id": "$job", "count": {"$sum": 1}}}
    ])), '../results/task2/t2_2_result')
json_dump(list(collection.aggregate([
        {"$group": {"_id": "$city", "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
    ])), '../results/task2/t2_3_result')
json_dump(list(collection.aggregate([
        {"$group": {"_id": "$job", "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
    ])), '../results/task2/t2_4_result')
json_dump(list(collection.aggregate([
        {"$group": {"_id": "$city", "min_age": {"$min": "$age"}, "avg_age": {"$avg": "$age"}, "max_age": {"$max": "$age"}}}
    ])), '../results/task2/t2_5_result')
json_dump(list(collection.aggregate([
        {"$group": {"_id": "$job", "min_age": {"$min": "$age"}, "avg_age": {"$avg": "$age"}, "max_age": {"$max": "$age"}}}
    ])), '../results/task2/t2_6_result')
json_dump(list(collection.aggregate([
        {"$group": {"_id": "$age", "max_salary": {"$max": "$salary"}}},
        {"$sort": {"_id": 1}},
        {"$limit": 1}
    ])), '../results/task2/t2_7_result')
json_dump(list(collection.aggregate([
        {"$group": {"_id": "$age", "min_salary": {"$min": "$salary"}}},
        {"$sort": {"_id": -1}},
        {"$limit": 1}
    ])), '../results/task2/t2_8_result')
json_dump(list(collection.aggregate([
        {"$match": {"salary": {"$gt": 50000}}},
        {"$group": {"_id": "$city", "min_age": {"$min": "$age"}, "avg_age": {"$avg": "$age"}, "max_age": {"$max": "$age"}}},
        {"$sort": {"_id": 1}}
    ])), '../results/task2/t2_9_result')
json_dump(list(collection.aggregate([
        {"$match": {"age": {"$in": list(range(18, 25)) + list(range(50, 65))}}},
        {"$group": {"_id": {"city": "$city", "job": "$job"}, "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
    ])), '../results/task2/t2_10_result')
json_dump(list(collection.aggregate([
        {"$match": {"city": "Астана", "job": "Строитель"}},
        {"$group": {"_id": "$year", "avg_salary": {"$avg": "$salary"}}},
        {"$sort": {"avg_salary": -1}}
    ])), '../results/task2/t2_11_result')
