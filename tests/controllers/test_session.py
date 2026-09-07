import pytest

from app.application_manager import ApplicationManager
from app.controllers.session import SessionController
from app.dtos.session import SessionDTO
from tests.setup.database import mock_client_db
from basic_components_fpp.exception import NotFoundAPI


def test_get_session_controller_instance():
    sessionController = ApplicationManager.get(SessionController, mock_client_db)
    assert sessionController.collection_name == SessionController.collection_name
    assert sessionController.client.HOST == mock_client_db.HOST


def test_session_controller_session_expired():
    sessionController = ApplicationManager.get(SessionController, mock_client_db)
    with pytest.raises(NotFoundAPI):
        sessionController.session_expired("Test test")


def test_session_controller_session_expired_success():
    sessionController = ApplicationManager.get(SessionController, mock_client_db)
    session = SessionDTO(token="test_token", user_id="123", user_name="Test User")

    created_session = sessionController.create(session)
    assert isinstance(created_session, SessionDTO)

    sessionController.session_expired("Bearer test_token")


def test_session_controller_create_session():
    sessionController = ApplicationManager.get(SessionController, mock_client_db)
    session = SessionDTO(token="test_token", user_id="123", user_name="Test User")

    created_session = sessionController.create(session)

    assert isinstance(created_session, SessionDTO)
    assert created_session.token == session.token
    assert created_session.user_id == session.user_id
    assert created_session.user_name == session.user_name
    assert created_session.id is not None
