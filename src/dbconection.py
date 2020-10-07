from conf import DB_URL, DB_NAME
from pymongo import MongoClient


client = MongoClient(DB_URL)

db = client.get_database(DB_NAME)