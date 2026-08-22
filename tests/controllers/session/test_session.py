from app.application_manager import ApplicationManager

from app.controllers.session import SessionController

from tests.controllers.session.variables import (
    SESSION_DTO_TEST,
)
from tests.setup.database import mock_client_db


class TestSession:
    sessionController = ApplicationManager.get(SessionController, mock_client_db)
    session_dto = SESSION_DTO_TEST

    def test_init_session_controller(self):
        collection_name = self.sessionController.collection_name
        assert collection_name == SessionController.collection_name
        assert self.sessionController.client == mock_client_db

    def test_create_session(self):
        result = self.sessionController.create(self.session_dto)
        assert self.session_dto.user_name == result.user_name
        assert self.session_dto.token == result.token

    def test_get_session_id(self):
        session_dto = self.sessionController.create(self.session_dto)
        id = session_dto.id
        result = self.sessionController.get_by_id(id=id)
        assert session_dto.user_name == result.user_name
        assert session_dto.token == result.token

    def test_get_filter_session(self):
        session_dto = self.sessionController.create(self.session_dto)
        result = self.sessionController.get_filter("token", session_dto.token)
        assert session_dto.user_name == result.user_name
        assert session_dto.token == result.token
