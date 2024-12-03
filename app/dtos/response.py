
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')

class ResponseDTO[T](BaseModel):
    data: T
    message: str
    status: str = "success"



class ResponseModelDTO[T](BaseModel):
    data: T
    message: str
    status: str = "success"



class ProductDTO(BaseModel):
    name: str
    price: str
    description: str