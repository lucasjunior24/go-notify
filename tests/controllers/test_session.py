import pytest

from app.application_manager import ApplicationManager
from app.controllers.session import SessionController
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
