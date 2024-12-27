from app.util.config import DB_URL

from pymongo import MongoClient

client = MongoClient(DB_URL)
