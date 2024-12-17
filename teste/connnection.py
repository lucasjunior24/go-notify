
from pymongo import MongoClient
from teste.config import IP_WITH_PORT_DB


client = MongoClient(f"mongodb://{IP_WITH_PORT_DB}")


database = client.get_database("model")