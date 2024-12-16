
from http import HTTPStatus
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar('T')

class ResponseDTO[T](BaseModel):
    data: T
    message: str = HTTPStatus(200).phrase
    status: str = "success"



class ResponseModelDTO(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    data: T
    message: str
    status: str = "success"





class UserModelDTO(BaseModel):
    id: str
    email: str
    name: str
    hashed_password: str
    disabled: bool
    _cls: str
    admin: bool
    admin_master: bool
    created_at: str
    updated_at: str
    session: list[dict]


class ReviewDTO(BaseModel):
    score: str
    comment: str
    photo: str



class CreateProductDTO(BaseModel):
    name: str
    price: str
    description: str
    review: ReviewDTO


class ProductModelDTO(BaseModel):
    id: str
    name: str
    price: str
    description: str
    created_at: str
    updated_at: str
    reviews: Optional[list[ReviewDTO]] = None


