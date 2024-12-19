
from app.util.config import DB_URL, DB_NAME

from pymongo import MongoClient

client = MongoClient(DB_URL)


database = client.get_database(DB_NAME)