from mongomock import MongoClient as MongoMockClient

from app.util.config import DB_URL

mock_client = MongoMockClient(DB_URL)
