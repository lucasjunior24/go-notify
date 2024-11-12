
from typing import TypeVar
from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar('T')

class ResponseDTO[T](BaseModel):
    data: T
    message: str
    status: str = "success"

