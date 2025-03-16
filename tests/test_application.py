# content of test_sample.py

from app.application_manager import ApplicationManager
from app.controllers.session import SessionController
from tests.setup.database import mock_client


def test_application():
    sessionController = ApplicationManager.get(SessionController, mock_client)
    assert sessionController.collection_name == SessionController.collection_name
    assert sessionController.client == mock_client
