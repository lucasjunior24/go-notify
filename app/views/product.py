from fastapi import APIRouter, Depends

from app.auth.token import get_token
from app.db.models.product import Product
from app.dtos.response import ProductDTO, ProductModelDTO, ResponseDTO, ResponseModelDTO


product_router = APIRouter(
    prefix="/product",
    tags=["Product"],
    dependencies=[Depends(get_token)],
    responses={404: {"description": "Not found"}},
)


@product_router.get("", response_model=ResponseModelDTO[ProductModelDTO])
async def read_system_status( name: str):
    product = Product.find('name', name)
    return ResponseDTO(data=product.to_json(), message="success")

@product_router.get("/all", response_model=ResponseModelDTO[list[ProductModelDTO]])
async def get_all():
    all_product = Product.get_all()
    all_product_json = [product.to_json() for product in all_product]
    return ResponseDTO(data=all_product_json, message="success")

@product_router.post("", response_model=ResponseModelDTO[ProductModelDTO])
async def create_product(
    product: ProductDTO,
):
    new_product = Product(name=product.name, price=product.price, description=product.description)
    new_product.save()
    return ResponseDTO(data=new_product.to_json(), message="success")



@product_router.delete("", response_model=ResponseModelDTO[ProductModelDTO])
async def delete(product_id: str):
    removed_product = Product.remove(id=product_id)
    return ResponseDTO(data=removed_product.to_json(), message="success")