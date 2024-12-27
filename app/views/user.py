from datetime import timedelta
from typing import Annotated
from app.db.models.user import UserDTO
from app.dtos.session import SessionDTO
from app.application_manager import applicationManager
from app.views import app
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from fastapi.security import (
    OAuth2PasswordRequestForm,
)

from app.auth.token import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_token,
)

from app.dtos.response import ResponseDTO, ResponseModelDTO
from app.dtos.user import Token, UserDBSessionDTO, createUserDTO


@app.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, expire = create_access_token(
        data={"sub": user.email, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    session = SessionDTO(
        token=access_token, expires_at=expire, user_name=user.name, user_id=str(user.id)
    )
    applicationManager.session_controller.create(session)
    return Token(access_token=access_token, token_type="bearer")


@app.get("/sessions", response_model=ResponseModelDTO[list[SessionDTO]])
async def read_users_me():

    all_sessions = applicationManager.session_controller.get_all()
    return ResponseDTO(data=all_sessions, message="success")


@app.get("/users/me/items/", response_model=ResponseModelDTO[list[dict]])
async def read_own_items():
    return ResponseDTO(data=[{"item_id": "Foo", "owner": "owner"}], message="success")


@app.get("/user", response_model=ResponseModelDTO[UserDTO])
async def read_system_status(
    token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)], email: str
):

    data = applicationManager.user_controller.get_filter("email", email)
    return ResponseDTO(data=data)


@app.get("/user/sessions", response_model=ResponseModelDTO[list[UserDBSessionDTO]])
async def read_system_status(
    token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)], user_id: str
):

    data = applicationManager.user_controller.get_user_with_sessions(user_id)
    return ResponseDTO(data=data)


@app.get("/user/refactor", response_model=ResponseModelDTO[UserDTO])
async def read_system_status(use_id: str):

    data = applicationManager.user_controller.get_by_id(use_id)
    return ResponseDTO(data=data)


@app.post(
    "/user",
    responses={201: {"model": ResponseModelDTO[UserDTO]}},
    response_model=ResponseModelDTO[UserDTO],
)
async def create(
    user: createUserDTO,
):
    hash = get_password_hash(user.password)
    user = UserDTO(email=user.email, name=user.username, hashed_password=hash)
    data = applicationManager.user_controller.create(user)

    return ResponseDTO(data=data)
