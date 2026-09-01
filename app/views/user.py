from typing import Annotated
from app.controllers.user import UserController
from app.db.models.user import UserDTO
from app.application_manager import ApplicationManager
from app.views import app
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends


from app.auth.token import (
    get_password_hash,
    get_token,
)

from app.dtos.response import ResponseDTO, ResponseModelDTO
from app.dtos.user import UserDBSessionDTO, createUserDTO


@app.get("/users/me/items/", response_model=ResponseModelDTO[list[dict]])
async def read_own_items():
    return ResponseDTO(data=[{"item_id": "Foo", "owner": "owner"}], message="success")


@app.get("/user", response_model=ResponseModelDTO[UserDTO])
async def get_user_by_email(
    token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)], email: str
):
    user_controller = ApplicationManager.get(UserController)
    data = user_controller.get_filter("email", email)
    return ResponseDTO(data=data)


@app.get("/user/session", response_model=ResponseModelDTO[list[UserDBSessionDTO]])
async def get_sessions_by_id(
    token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)], user_id: str
):
    print(token)
    user_controller = ApplicationManager.get(UserController)
    data = user_controller.get_user_with_sessions(user_id)
    return ResponseDTO(data=data)


@app.get("/user/refactor", response_model=ResponseModelDTO[UserDTO])
async def get_user_by_id(user_id: str):
    user_controller = ApplicationManager.get(UserController)
    data = user_controller.get_by_id(user_id)
    return ResponseDTO(data=data)


@app.post(
    "/user",
    responses={201: {"model": ResponseModelDTO[UserDTO]}},
    response_model=ResponseModelDTO[UserDTO],
)
async def create(
    user: createUserDTO,
):
    user_controller = ApplicationManager.get(UserController)
    hash = get_password_hash(user.password)
    user = UserDTO(email=user.email, name=user.username, hashed_password=hash)
    data = user_controller.create(user)
    return ResponseDTO(data=data)
