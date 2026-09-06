from app.services.chat_ai_service import ChatAIService

from tests.services.chat_ai.variables import USER_ID, RequestMock


class TestChatAI:
    chat_ai_service = ChatAIService(url="test", request=RequestMock)

    def test_init_chat_ai_service(self):
        assert "test" == self.chat_ai_service.url

    def test_send_message(self):
        chat = self.chat_ai_service.send_message("TESTE")
        assert USER_ID == chat.user_id
