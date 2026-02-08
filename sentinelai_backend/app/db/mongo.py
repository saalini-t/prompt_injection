from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["sentinelai"]
attack_logs = db["attack_logs"]
