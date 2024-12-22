from pydantic import Field

from app.dtos.base import DTO


class UserDTO(DTO):
    email: str = Field(default='')
    name: str = Field(default='')
    hashed_password: str = Field(default='')
    disabled: bool = Field(default=False)
    admin: bool = Field(default=False)
    admin_master: bool = Field(default=False)


