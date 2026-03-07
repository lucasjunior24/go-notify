from http import HTTPStatus
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.v1 import Field

from app.dtos.base import BaseDTO, CustomObjectId


T = TypeVar("T")


class ResponseDTO[T](BaseModel):
    data: T
    message: str = HTTPStatus(200).phrase
    status: str = "success"


class ResponseModelDTO(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    data: T
    message: str
    status: str = "success"


class CreateReviewDTO(BaseModel):
    score: str
    comment: str
    photo: str


class CreateProductDTO(BaseModel):
    name: str
    price: str
    description: str
    reviews: list[CreateReviewDTO] = Field(default_factory=list)


class EditReviewDTO(CreateReviewDTO):
    id: str


class EditProductDTO(CreateProductDTO):
    reviews: list[EditReviewDTO] = Field(default_factory=list)
