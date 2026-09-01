from fastapi import APIRouter, Depends
from bson import ObjectId

from app.application_manager import ApplicationManager
from app.auth.token import get_token
from app.controllers.product import ProductController
from app.db.models.product import ProductDTO

from app.db.models.reviews import ReviewDTO

from app.dtos.base import CustomObjectId
from app.dtos.response import (
    CreateProductDTO,
    CreateReviewDTO,
    EditProductDTO,
    ResponseDTO,
    ResponseModelDTO,
)

product_router = APIRouter(
    prefix="/product",
    tags=["Product"],
    dependencies=[Depends(get_token)],
    responses={404: {"description": "Not found"}},
)


@product_router.get("/{id}", response_model=ResponseModelDTO[ProductDTO])
async def get_by_id(id: str):
    product_controller = ApplicationManager.get(ProductController)
    product = product_controller.get_by_id(id)
    return ResponseDTO(data=product, message="success")


@product_router.get("", response_model=ResponseModelDTO[ProductDTO])
async def get_filter(key: str, name: str):
    product_controller = ApplicationManager.get(ProductController)
    product = product_controller.get_filter(key, name)
    return ResponseDTO(data=product, message="success")


@product_router.get("/all", response_model=ResponseModelDTO[list[ProductDTO]])
async def get_all():
    product_controller = ApplicationManager.get(ProductController)
    all_product = product_controller.get_all()
    return ResponseDTO(data=all_product, message="success")


@product_router.post("", response_model=ResponseModelDTO[ProductDTO])
async def create_product(
    product: CreateProductDTO,
):
    product_controller = ApplicationManager.get(ProductController)
    product_dto = ProductDTO(**product.model_dump())
    for review in product_dto.reviews:
        review.id = CustomObjectId()
    new_product = product_controller.create(product_dto)
    return ResponseDTO(data=new_product, message="success")


@product_router.put("", response_model=ResponseModelDTO[ProductDTO])
async def update(
    id: str,
    product: EditProductDTO,
):
    product_controller = ApplicationManager.get(ProductController)
    product_dto = ProductDTO(**product.model_dump())
    product_updated = product_controller.update(id, product_dto)
    return ResponseDTO(data=product_updated, message="success")


@product_router.delete("/{id}", response_model=ResponseModelDTO[bool])
async def delete(id: str):
    product_controller = ApplicationManager.get(ProductController)
    is_removed = product_controller.remove(id=id)
    return ResponseDTO(data=is_removed, message="success")


@product_router.post("/review", response_model=ResponseModelDTO[ProductDTO])
async def add_review(review_dto: CreateReviewDTO, product_id: str):
    product_controller = ApplicationManager.get(ProductController)
    product = product_controller.get_by_id(id=product_id)
    new_review = ReviewDTO(**review_dto.model_dump(), _id=ObjectId())
    product.reviews.append(new_review)
    product_updated = product_controller.update(product_id, product)
    return ResponseDTO(data=product_updated, message="success")
