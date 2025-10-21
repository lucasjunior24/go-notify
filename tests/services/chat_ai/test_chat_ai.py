from app.services.chat_ai_service import ChatAIService

from tests.services.chat_ai.variables import USER_ID, RequestMock


class TestChatAI:
    chat_ai_service = ChatAIService(url="test", request=RequestMock)

    def test_init_chat_ai_service(self):
        assert "test" == self.chat_ai_service.url

    def test_send_message(self):
        result = self.chat_ai_service.send_message("TESTE")
        assert USER_ID == result.user_id

    # def test_get_session_id(self):
    #     session_dto = self.sessionController.create(self.session_dto)
    #     id = session_dto.id
    #     result = self.sessionController.get_by_id(id=id)
    #     assert session_dto.user_name == result.user_name
    #     assert session_dto.token == result.token
