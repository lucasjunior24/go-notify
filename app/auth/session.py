
from pydantic import BaseModel
import uuid

from app.db.models.session import Session

class SessionDTO(BaseModel):
  id: str
  access_token: str
  username: str

class ManagerSession(BaseModel):
  sessions: list[SessionDTO] = []

  def validate_token(self, token: str):
    type, hash = token.split(" ")
    tokens = Session.get_session_by_token(hash)
    return bool(tokens)

manager = ManagerSession()


def create_session(access_token: str, username: str):
  session = SessionDTO(access_token=access_token, username=username, id=str(uuid.uuid1()))
  manager.sessions.append(session)
  return session



