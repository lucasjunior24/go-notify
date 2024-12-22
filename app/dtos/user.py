from pydantic import BaseModel, Field

from app.dtos.base import DTO
from app.dtos.session import SessionDBDTO


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class createUserDTO(BaseModel):
    username: str
    email: str
    password: str


class UserDBSessionDTO(DTO):
    email: str = Field(default="")
    name: str = Field(default="")
    hashed_password: str = Field(default="")
    disabled: bool = Field(default=False)
    admin: bool = Field(default=False)
    admin_master: bool = Field(default=False)
    session: list[SessionDBDTO] = Field(...)
