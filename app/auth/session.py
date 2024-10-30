from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel
import uuid

class Session(BaseModel):
  id: str
  access_token: str
  username: str

class ManagerSession(BaseModel):
  sessions: list[Session] = []

  def validate_token(self, token: str):
    tokens = list(filter(lambda s: (s.access_token == token), self.sessions))
    return bool(tokens)

manager = ManagerSession()

def get_session(session: Session):
    with manager.sessions:
        yield session

def create_session(access_token: str, username: str):
  session = Session(access_token=access_token, username=username, id=str(uuid.uuid1()))
  manager.sessions.append(session)
  return session





SessionDep = Annotated[Session, Depends(get_session)]

