from pydantic import Field


from app.db.models.reviews import ReviewDTO
from app.dtos.base import DTO


class ProductDTO(DTO):
    price: str = Field(default="")
    name: str = Field(default="")
    description: str = Field(default="")

    reviews: list[ReviewDTO] = Field(default_factory=list)
