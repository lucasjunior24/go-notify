from datetime import datetime
from typing import Optional

from pymongo import MongoClient
from app.controllers.base import BaseController
from app.dtos.session import SessionDTO


class SessionController(BaseController[SessionDTO]):
    collection_name = "session"

    def __init__(
        self, dto: SessionDTO = SessionDTO, _client: MongoClient | None = None
    ):
        super().__init__(dto, _client)

    def session_expired(self, token: str) -> bool:
        type, token = token.split(" ")
        session: SessionDTO = self.get_filter("token", token)
        if session is None:
            return True
        now = datetime.now().replace(tzinfo=None)
        expire = session.expires_at.replace(tzinfo=None) <= now

        return expire
