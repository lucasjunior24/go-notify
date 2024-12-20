
from datetime import datetime
from app.controllers.base import BaseController
from app.dtos.session import SessionDBDTO

class SessionController(BaseController):
  def __init__(self, collection = "session", dto = SessionDBDTO):
    super().__init__(collection, dto)



  def session_expired(self, token: str) -> bool:
      type, token = token.split(" ")
      session: SessionDBDTO = self.get_filter("token", token)
      if session is None:
          return True
      now = datetime.now().replace(tzinfo=None)
      expire = session.expires_at.replace(tzinfo=None) <= now

      return expire