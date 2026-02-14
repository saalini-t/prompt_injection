import os
from pymongo import MongoClient

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
mongo_db_name = os.getenv("MONGO_DB", "sentinelai")

client = MongoClient(mongo_uri)

db = client[mongo_db_name]
attack_logs = db["attack_logs"]
