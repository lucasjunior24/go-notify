from mongomock import MongoClient as MongoMockClient

DB_URL = f"mongodb://localhost"

mock_client_db = MongoMockClient(DB_URL)
