from app.dtos.base import CustomObjectId
from app.util.request import Request
from typing import override

from app.util.requestsDTOs.chat import ChatDTO


USER_ID = "teste_1"

chat_dto = ChatDTO(
    created_by="",
    messages=[],
    updated_by="",
    user_id=USER_ID,
)


class RequestMock(Request):
    def __init__(self, url):
        super().__init__(url)

    @override
    def post(self, params, route, dto):
        return chat_dto
