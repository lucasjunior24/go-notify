from datetime import datetime
from typing import Optional
from pydantic import Field

from app.dtos.base import BaseDTO, CustomObjectId


class MessageDTO(BaseDTO):
    id: Optional[CustomObjectId] = Field(alias="_id", default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    author: str = Field(default="")
    message: str = Field(default="")
