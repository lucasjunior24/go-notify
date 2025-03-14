# content of test_sample.py

from app.application_manager import ApplicationManager
from app.controllers.session import SessionController


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4


def test_application():
    DB_NAME = "unit_test_go_notify"
    sessionController = ApplicationManager.get(SessionController, DB_NAME)
    assert sessionController.collection_name == SessionController.collection_name
    assert sessionController.db_name == DB_NAME
