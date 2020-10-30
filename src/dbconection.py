from conf import DB_URI, DB_NAME
from pymongo import MongoClient


client = MongoClient(DB_URI)

db = client.get_database(DB_NAME)
