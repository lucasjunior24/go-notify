from pydantic import BaseModel, Field

from app.dtos.base import DTO
from app.dtos.session import SessionDTO


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
    session: list[SessionDTO] = Field(...)

    @staticmethod
    def get_user_with_sessions(user_id: str):
        query = [
            {"$addFields": {"id": {"$toString": "$_id"}}},
            {"$match": {"id": user_id}},
            {
                "$lookup": {
                    "from": "session",
                    "localField": "id",
                    "foreignField": "user_id",
                    "as": "session",
                }
            },
        ]
        return query
