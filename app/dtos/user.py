
from pydantic import BaseModel, Field

from app.dtos.base import DTO




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


class UserDBDTO(DTO):
    email: str = Field(default='')
    name: str = Field(default='')
    hashed_password: str = Field(default='')
    disabled: bool = Field(default=False)
    admin: bool = Field(default=False)
    admin_master: bool = Field(default=False)

