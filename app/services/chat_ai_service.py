from typing import TypeVar
from app.controllers.base import V
from app.dtos.response import T
from app.util.request import Request
from app.util.config import CHAT_API_URL
from app.util.requestsDTOs.chat import ChatDTO


class ChatAIService:
    def __init__(self, request: Request | None = None):
        self.request: Request = request or Request(url=CHAT_API_URL)

    def send_message(self, message: str) -> ChatDTO:
        params = {"message": message}
        response = self.request.post(params=params, route="/chats/message", dto=ChatDTO)
        return response
