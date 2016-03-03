import pymongo
import json

from pymongo import MongoClient

client = MongoClient()
client = MongoClient("localhost", 27017)

db = client.test_db

collection = db.test_collection

mydict = {"name": "Lucy", "sex": "female", "job": "nurse"}

collection.insert(mydict)
collection.insert({"name": "Lucy", "sex": "female", "job": "nurse"})
collection.insert({"name": "Tom", "sex": "female", "job": "nurse"})
collection.insert({"name": "Oscar", "sex": "female", "job": "nurse"})

mylist = []
mylist.append(mydict)

# collection.insert_many(mylist)
doc = collection.find_one({"name": "Lucy"})
print doc

del doc["_id"]
json.dump(doc)
