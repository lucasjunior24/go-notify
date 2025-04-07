from typing import TypeVar
from app.controllers.base import V
from app.dtos.response import T
from app.util.request import Request
from app.util.config import CHAT_API_URL
from app.util.requestsDTOs.chat import ChatDTO


class ChatAIService:
    def __init__(self, url: str = CHAT_API_URL, request: Request = Request):
        self.url = url
        self.request: Request = request(url=self.url)

    def send_message(self, message: str) -> ChatDTO:
        params = {"message": message}
        response = self.request.post(params=params, route="/chats/message", dto=ChatDTO)
        return response
