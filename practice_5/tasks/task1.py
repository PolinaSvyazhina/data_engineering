import pymongo

from utils.generalPurposeReader import get_object_list
from utils.jsonDumper import json_dump

client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db = client.test_database
collection = db.example_collection

collection.insert_many(get_object_list('../data/task_1_item.text'))

json_dump(list(collection.find().sort("salary", -1).limit(10)), '../results/task1/t1_1_result')
json_dump(list(collection.find({'age': {'$lt': 30}}).sort("salary", -1).limit(15)), '../results/task1/t1_2_result')
json_dump(list(collection.find({"city": "Виго", "job": {"$in": ["Инженер", "Медсестра", "Водитель"]}}).sort("age", pymongo.ASCENDING).limit(10)), '../results/task1/t1_3_result')
json_dump(collection.count_documents(
        {"age": {"$gte": 10, "$lte": 48},
         "year": {"$in": [2019, 2020, 2021, 2022]},
         "$or": [
             {"salary": {"$gt": 50000, "$lte": 75000}},
             {"salary": {"$gt": 125000, "$lt": 150000}}
         ]}
    ), '../results/task1/t1_4_result')

