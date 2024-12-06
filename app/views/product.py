from fastapi import APIRouter, Depends

from app.auth.token import get_token
from app.db.models.product import Product
from app.dtos.response import ProductDTO, ResponseDTO

product_router = APIRouter(
    prefix="/product",
    tags=["Product"],
    dependencies=[Depends(get_token)],
    responses={404: {"description": "Not found"}},
)
@product_router.get("/all")
async def get_all():
    return {"message": "Product"}

@product_router.post("")
async def create_product(
    product: ProductDTO,
):
    new_product = Product(name=product.name, price=product.price, description=product.description)
    new_product.save()
    return ResponseDTO(data=new_product.to_json(), message="success")

