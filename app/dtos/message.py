from datetime import datetime

from pydantic import Field

from app.dtos.base import BaseDTO


class MessageDTO(BaseDTO):
    created_at: datetime = Field(default_factory=datetime.now)
    author: str = Field(default="")
    message: str = Field(default="")
