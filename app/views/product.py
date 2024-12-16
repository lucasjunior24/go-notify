from fastapi import APIRouter, Depends

from app.auth.token import get_token
from app.db.models.product import Product
from app.db.models.reviews import Review
from app.dtos.response import CreateProductDTO, ProductModelDTO, ResponseDTO, ResponseModelDTO, ReviewDTO
from app.util.schema.product import product_schema

product_router = APIRouter(
    prefix="/product",
    tags=["Product"],
    dependencies=[Depends(get_token)],
    responses={404: {"description": "Not found"}},
)


@product_router.get("", response_model=ResponseModelDTO[ProductModelDTO])
async def read_system_status( key: str, name: str):
    product = Product.find(key, name)
    dump_data = product_schema.dump(product)
    return ResponseDTO(data=dump_data, message="success")

@product_router.get("/all", response_model=ResponseModelDTO[list[ProductModelDTO]])
async def get_all():
    all_product = Product.get_all()
    dump_data = [product_schema.dump(product) for product in all_product]
    return ResponseDTO(data=dump_data, message="success")

@product_router.post("", response_model=ResponseModelDTO[ProductModelDTO])
async def create_product(
    product: CreateProductDTO,
):
    new_product = Product(name=product.name, price=product.price, description=product.description)
    new_review = Review(**product.review.model_dump())
    new_product.reviews.append(new_review)
    new_product.save()
    dump_data = product_schema.dump(new_product)
    return ResponseDTO(data=dump_data, message="success")

@product_router.put("", response_model=ResponseModelDTO[ProductModelDTO])
async def update(
    id: str,
    product: CreateProductDTO,
):
    product_json = product.model_dump()
    product = Product.update(id=id, value=product_json)
    dump_data = product_schema.dump(product)
    return ResponseDTO(data=dump_data, message="success")


@product_router.delete("", response_model=ResponseModelDTO[ProductModelDTO])
async def delete(product_id: str):
    removed_product = Product.remove(id=product_id)
    return ResponseDTO(data=removed_product.to_json(), message="success")


@product_router.post("/review", response_model=ResponseModelDTO[ProductModelDTO])
async def create_product(
    review_dto: ReviewDTO,
    product_id: str
):
    product = Product.get_by_id(product_id)
    new_review = Review(**review_dto.model_dump())
    product.reviews.append(new_review)
    product.save()
    dump_data = product_schema.dump(product)
    return ResponseDTO(data=dump_data, message="success")