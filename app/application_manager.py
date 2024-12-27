from pymongo import MongoClient
from typing import Optional
from app.controllers.session import SessionController
from app.controllers.user import UserController
from app.util.config import DB_NAME
from app.db.connection import client


class ApplicationManager:
    def __init__(self, _client: Optional[MongoClient] = None):
        if _client is None:
            _client = client
        database = _client.get_database(DB_NAME)
        self.user_controller = UserController(collection=database["user"])
        self.session_controller = SessionController(collection=database["session"])


applicationManager = ApplicationManager()
