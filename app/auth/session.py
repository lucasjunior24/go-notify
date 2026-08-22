from pydantic import BaseModel
import uuid


class SessionMDTO(BaseModel):
    id: str
    access_token: str
    username: str


def create_session(access_token: str, username: str):
    session = SessionMDTO(
        access_token=access_token, username=username, id=str(uuid.uuid1())
    )

    return session
