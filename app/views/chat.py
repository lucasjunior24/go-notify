from fastapi import APIRouter, Depends

from app.auth.token import get_token
from app.db.models.product import Product
from app.db.models.reviews import Review
from app.dtos.response import (
    CreateProductDTO,
    ProductModelDTO,
    ResponseDTO,
    ResponseModelDTO,
)
from app.services.chat_ai_service import ChatAIService
from app.util.requestsDTOs.chat import ChatDTO
from app.util.schema.product import product_schema

chat_ai_router = APIRouter(
    prefix="/chat_ai",
    tags=["Chat AI"],
    # dependencies=[Depends(get_token)],
    responses={404: {"description": "Not found"}},
)


@chat_ai_router.get("", response_model=ResponseModelDTO[ProductModelDTO])
async def read_system_status(key: str, name: str):
    product = Product.find(key, name)
    dump_data = product_schema.dump(product)
    return ResponseDTO(data=dump_data, message="success")


@chat_ai_router.get("/all", response_model=ResponseModelDTO[list[ProductModelDTO]])
async def get_all():
    all_product = Product.get_all()
    dump_data = [product_schema.dump(product) for product in all_product]
    return ResponseDTO(data=dump_data, message="success")


@chat_ai_router.post(
    "/message",
    responses={201: {"model": ResponseModelDTO[ChatDTO]}},
    response_model=ResponseModelDTO[ChatDTO],
)
async def message(message: str, chat_id: str | None = None):
    message_service = ChatAIService()
    data = message_service.send_message(message=message)
    return ResponseDTO(data=data)
