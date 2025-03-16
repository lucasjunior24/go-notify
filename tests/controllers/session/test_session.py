from datetime import datetime, timezone

from fastapi.security import HTTPAuthorizationCredentials
from app.application_manager import ApplicationManager
from app.auth.token import ValidateToken
from app.controllers.session import SessionController
from app.dtos.session import SessionDTO
from tests.controllers.session.variables import (
    BEARER_TOKEN_TEST,
    SESSION_DTO_TEST,
    TOKEN_TEST,
)
from tests.setup.database import mock_client


class TestSession:
    sessionController = ApplicationManager.get(SessionController, mock_client)
    session_dto = SESSION_DTO_TEST

    def test_init_session_controller(self):
        collection_name = self.sessionController.collection_name
        assert collection_name == SessionController.collection_name
        assert self.sessionController.client == mock_client

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

    def test_validate_token(self):
        auth = HTTPAuthorizationCredentials(credentials=BEARER_TOKEN_TEST, scheme="")

        self.sessionController.create(self.session_dto)
        validateToken = ValidateToken(auth)
        validateToken.sessionController = self.sessionController

        assert validateToken.auth.credentials == BEARER_TOKEN_TEST
