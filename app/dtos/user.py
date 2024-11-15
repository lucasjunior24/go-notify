
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class UserDTO(BaseModel):
    username: str
    email: str
    password: str


class UserInDB(UserDTO):
    hashed_password: str
