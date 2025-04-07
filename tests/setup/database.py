from mongomock import MongoClient as MongoMockClient

DB_URL = f"mongodb://localhost"

mock_client = MongoMockClient(DB_URL)
