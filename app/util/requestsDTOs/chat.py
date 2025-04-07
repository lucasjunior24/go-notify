from pydantic import Field


from app.dtos.base import DTO
from .message import MessageDTO


class ChatDTO(DTO):
    messages: list[MessageDTO] = Field(default_factory=list)
    user_id: str = Field(default="")
