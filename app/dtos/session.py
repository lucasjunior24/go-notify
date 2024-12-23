from datetime import datetime
from pydantic import Field
from app.dtos.base import DTO


class SessionDTO(DTO):
    token: str = Field(default="")
    user_id: str = Field(default="")
    user_name: str = Field(default="")
    expires_at: datetime = Field(default_factory=datetime.now)
