from app.application_manager import ApplicationManager
from app.controllers.session import SessionController
from tests.setup.database import mock_client_db


def test_application_get_session_controller():
    sessionController = ApplicationManager.get(SessionController, mock_client_db)
    assert sessionController.collection_name == SessionController.collection_name
    assert sessionController.client.HOST == mock_client_db.HOST
