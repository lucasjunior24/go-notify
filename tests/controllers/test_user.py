from unittest.mock import patch

from app.controllers.user import UserController
from app.dtos.user import UserDBSessionDTO
from tests.setup.database import mock_client_db


def test_get_user_controller_instance():
    user_controller = UserController(_client=mock_client_db)
    assert user_controller.collection_name == "user"
    assert user_controller.client.HOST == mock_client_db.HOST


def test_get_user_with_sessions_calls_get_with_query():
    user_controller = UserController(_client=mock_client_db)
    user_id = "user-123"

    expected_query = UserDBSessionDTO.get_user_with_sessions(user_id=user_id)
    expected_users = [UserDBSessionDTO(session=[])]

    with patch.object(
        user_controller, "get_with_query", return_value=expected_users
    ) as mock_get_with_query:
        users = user_controller.get_user_with_sessions(user_id)

    mock_get_with_query.assert_called_once_with(
        data=expected_query, dto=UserDBSessionDTO
    )
    assert users == expected_users


def test_get_user_with_sessions_returns_empty_list_when_no_users():
    user_controller = UserController(_client=mock_client_db)
    user_id = "user-123"

    with patch.object(user_controller, "get_with_query", return_value=[]) as mock_get:
        users = user_controller.get_user_with_sessions(user_id)

    assert users == []
