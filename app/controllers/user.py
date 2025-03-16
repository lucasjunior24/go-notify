from typing import Optional
from pymongo import MongoClient
from app.controllers.base import BaseController
from app.db.models.user import UserDTO
from app.dtos.user import UserDBSessionDTO


class UserController(BaseController[UserDTO]):
    collection_name = "user"

    def __init__(self, dto: UserDTO = UserDTO, _client: MongoClient | None = None):
        super().__init__(dto, _client)

    def get_user_with_sessions(self, user_id: str):
        users = self.get_with_query(
            data=UserDBSessionDTO.get_user_with_sessions(user_id=user_id),
            dto=UserDBSessionDTO,
        )
        return users
