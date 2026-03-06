from mongoengine import *
from pydantic import Field

from app.dtos.base import DTO
class ReviewDTO(DTO):
    score: str = Field(default="")
    comment: str = Field(default="")
    photo: str = Field(default="")
