
from datetime import datetime
from app.controllers.base import BaseController

class SessionController(BaseController):
  def __init__(self, collection = "session"):
    super().__init__(collection)


  @classmethod
  def session_expired(cls, token: str) -> bool:
      type, token = token.split(" ")
      session = cls.get_filter("token", token)
      if session is None:
          return True
      now = datetime.now()
      expire = bool(session.expires_at <= now)

      return expire