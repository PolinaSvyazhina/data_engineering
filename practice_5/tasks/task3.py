import pymongo

from utils.generalPurposeReader import get_object_list
from utils.jsonDumper import json_dump

client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db = client.test_database
collection = db.example_collection

collection.insert_many(get_object_list('../data/task_3_item.csv'))

selected_jobs = ["Медсестра", "Учитель"]
selected_cities = ["Куэнка", "Сория"]

collection.delete_many({"$or": [{"salary": {"$lt": 25000}}, {"salary": {"$gt": 175000}}]})
json_dump(list(collection.find()), '../results/task3/t3_1_result')
collection.update_many({}, {"$inc": {"age": 1}})
json_dump(list(collection.find()), '../results/task3/t3_2_result')
collection.update_many({"job": {"$in": selected_jobs}}, {"$mul": {"salary": 1.05}})
json_dump(list(collection.find()), '../results/task3/t3_3_result')
collection.update_many({"city": {"$in": selected_cities}}, {"$mul": {"salary": 1.07}})
json_dump(list(collection.find()), '../results/task3/t3_4_result')

selected_predicate = {"city": "Тбилиси", "job": {"$in": ["Менеджер", "Программист"]}, "age": {"$gte": 30, "$lte": 50}}
collection.update_many(selected_predicate, {"$mul": {"salary": 1.1}})
json_dump(list(collection.find()), '../results/task3/t3_5_result')

delete_predicate = {"year": {"$lt": 2001}}
collection.delete_many(delete_predicate)

json_dump(list(collection.find()), '../results/task3/t3_6_result')
