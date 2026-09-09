from app.services.chat_ai_service import ChatAIService

from tests.services.chat_ai.variables import USER_ID, RequestMock


class TestChatAI:
    URL_TEST = "test"
    request = RequestMock(url=URL_TEST)
    chat_ai_service = ChatAIService(request=request)

    def test_init_chat_ai_service(self):
        assert self.URL_TEST == self.chat_ai_service.request.url

    def test_send_message(self):
        chat = self.chat_ai_service.send_message("TESTE")
        assert USER_ID == chat.user_id
