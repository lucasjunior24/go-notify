
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')

class ResponseDTO[T](BaseModel):
    data: T
    message: str
    status: str = "success"



class ResponseModelDTO(BaseModel, Generic[T]):
    data: T
    message: str
    status: str = "success"



class ProductDTO(BaseModel):
    name: str
    price: str
    description: str


class UserModelDTO(BaseModel):
    id: str
    email: str
    name: str
    hashed_password: str
    disabled: bool
    admin: bool
    admin_master: bool
    created_at: str
    updated_at: str