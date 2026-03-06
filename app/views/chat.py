from fastapi import APIRouter, Depends

from app.auth.token import get_token
from app.dtos.response import (
    ProductModelDTO,
    ResponseDTO,
    ResponseModelDTO,
)
from app.services.chat_ai_service import ChatAIService
from app.util.requestsDTOs.chat import ChatDTO


chat_ai_router = APIRouter(
    prefix="/chat_ai",
    tags=["Chat AI"],
    dependencies=[Depends(get_token)],
    responses={404: {"description": "Not found"}},
)


@chat_ai_router.get("", response_model=ResponseModelDTO[ProductModelDTO])
async def read_system_status(key: str, name: str):
    return ResponseDTO(data=key, message="success")


@chat_ai_router.get("/all", response_model=ResponseModelDTO[list[ProductModelDTO]])
async def get_all():
    return ResponseDTO(data=[], message="success")


@chat_ai_router.post(
    "/message",
    responses={201: {"model": ResponseModelDTO[ChatDTO]}},
    response_model=ResponseModelDTO[ChatDTO],
)
async def message(message: str, chat_id: str | None = None):
    message_service = ChatAIService()
    data = message_service.send_message(message=message)
    return ResponseDTO(data=data)
