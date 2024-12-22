from pydantic import BaseModel
import uuid


class SessionDTO(BaseModel):
    id: str
    access_token: str
    username: str


class ManagerSession(BaseModel):
    sessions: list[SessionDTO] = []

    def validate_token(self, token: str): ...


manager = ManagerSession()


def create_session(access_token: str, username: str):
    session = SessionDTO(
        access_token=access_token, username=username, id=str(uuid.uuid1())
    )
    manager.sessions.append(session)
    return session
