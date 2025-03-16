from datetime import datetime, timezone
from app.application_manager import ApplicationManager
from app.controllers.session import SessionController
from app.dtos.session import SessionDTO
from tests.setup.database import mock_client


def test_init_session_controller():
    sessionController = ApplicationManager.get(SessionController, mock_client)
    assert sessionController.collection_name == SessionController.collection_name
    assert sessionController.client == mock_client


def test_create_session():
    sessionController = ApplicationManager.get(SessionController, mock_client)
    session_dto = SessionDTO(
        token="test",
        expires_at=datetime.now(timezone.utc),
        user_name="lucas",
        user_id="",
    )
    result = sessionController.create(session_dto)
    assert session_dto.user_name == result.user_name
    assert session_dto.token == result.token
