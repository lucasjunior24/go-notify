from fastapi import APIRouter, Depends

from app.application_manager import ApplicationManager
from app.auth.token import get_token
from app.controllers.product import ProductController
from app.db.models.product import ProductDTO, ProductDTO

from app.dtos.response import (
    CreateProductDTO,
    ProductModelDTO,
    ResponseDTO,
    ResponseModelDTO,
)

product_router = APIRouter(
    prefix="/product",
    tags=["Product"],
    dependencies=[Depends(get_token)],
    responses={404: {"description": "Not found"}},
)


@product_router.get("", response_model=ResponseModelDTO[ProductModelDTO])
async def read_system_status(key: str, name: str):
    product_controller = ApplicationManager.get(ProductController)
    product = product_controller.find(key, name)
    return ResponseDTO(data=product, message="success")


@product_router.get("/all", response_model=ResponseModelDTO[list[ProductModelDTO]])
async def get_all():
    product_controller = ApplicationManager.get(ProductController)
    all_product = product_controller.get_all()
    return ResponseDTO(data=all_product, message="success")


@product_router.post("", response_model=ResponseModelDTO[ProductDTO])
async def create_product(
    product: CreateProductDTO,
):
    product_controller = ApplicationManager.get(ProductController)
    new_product = product_controller.create(product)
    return ResponseDTO(data=new_product, message="success")


# @product_router.put("", response_model=ResponseModelDTO[ProductModelDTO])
# async def update(
#     id: str,
#     product: CreateProductDTO,
# ):
#     product_controller = ApplicationManager.get(ProductController)
#     product_json = product.model_dump()
#     product = Product.update(id=id, value=product_json)
#     dump_data = product_schema.dump(product)
#     return ResponseDTO(data=dump_data, message="success")


# @product_router.delete("", response_model=ResponseModelDTO[ProductModelDTO])
# async def delete(product_id: str):
#     removed_product = Product.remove(id=product_id)
#     return ResponseDTO(data=removed_product.to_json(), message="success")


# @product_router.post("/review", response_model=ResponseModelDTO[ProductModelDTO])
# async def create_product(review_dto: ReviewDTO, product_id: str):
#     product = Product.get_by_id(product_id)
#     new_review = Review(**review_dto.model_dump())
#     product.reviews.append(new_review)
#     product.save()
#     dump_data = product_schema.dump(product)
#     return ResponseDTO(data=dump_data, message="success")
