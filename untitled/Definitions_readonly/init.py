import pymongo

from pymongo import MongoClient
conn = MongoClient("localhost", 27017)
'''
db = conn.example
db.words.insert({"word": "oarlock", "definition": "A device attached to a rowboat to hold the oars in place"})
db.words.insert({"word": "seminomadic", "definition": "Only partially nomadic"})
db.words.insert({"word": "perturb", "definition": "Bother, unsettle, modify"})
'''

db = conn.definitions
db.words.insert({"definition": "a leg shirt", "word": "pants"})