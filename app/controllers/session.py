from datetime import datetime
from app.controllers.base import BaseController
from app.dtos.session import SessionDTO


class SessionController(BaseController[SessionDTO]):
    def __init__(self, collection_name="session", dto=SessionDTO, collection=None):
        super().__init__(collection_name, dto, collection)

    def session_expired(self, token: str) -> bool:
        type, token = token.split(" ")
        session: SessionDTO = self.get_filter("token", token)
        if session is None:
            return True
        now = datetime.now().replace(tzinfo=None)
        expire = session.expires_at.replace(tzinfo=None) <= now

        return expire


sessionController = SessionController()
