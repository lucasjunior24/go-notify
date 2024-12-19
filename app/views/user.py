
from datetime import timedelta
from typing import Annotated
from app.controllers.base import BaseController
from app.util.schema.user import user_schema
from app.views import app
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import  Depends, HTTPException
from fastapi.security import (
    OAuth2PasswordRequestForm,
)

from app.auth.token import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_password_hash, get_token
from app.db.models.session import Session
from app.db.models.user import User
from app.dtos.response import ResponseDTO, ResponseModelDTO, UserModelDTO
from app.dtos.user import Token, UserDBDTO, UserDTO


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
    Session.create(token=access_token, expires_at=expire, user_name=user.name, user_id=str(user.id))
    return Token(access_token=access_token, token_type="bearer")


@app.get("/sessions", response_model=ResponseModelDTO[list[dict]])
async def read_users_me():

    all_sessions = Session.get_all()
    all_sessions_json = [session.to_json() for session in all_sessions]
    return ResponseDTO(data=all_sessions_json, message="success")


@app.get("/users/me/items/", response_model=ResponseModelDTO[list[dict]])
async def read_own_items(
    ):
    return ResponseDTO(data=[{"item_id": "Foo", "owner": 'owner'}], message="success")


@app.get("/user", response_model=ResponseModelDTO[UserModelDTO])
async def read_system_status(token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)], email: str):
    user = User.find('email', email)
    return ResponseDTO(data=user.to_json())


@app.get("/user/sessions", response_model=ResponseModelDTO[list[UserModelDTO]])
async def read_system_status(token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)], email: str):
    users = User.get_user_with_sessions(email)
    dump_data = [user_schema.dump(user) for user in users]
    return ResponseDTO(data=dump_data)


@app.get("/user/refactor", response_model=ResponseModelDTO[UserDBDTO])
async def read_system_status(use_id: str):
    
    base = BaseController("user")
    data = base.get_by_id(use_id, UserDBDTO)
    return ResponseDTO(data=data)


@app.post("/user",responses={201: {"model": ResponseModelDTO[UserModelDTO]}}, response_model=ResponseModelDTO[UserDBDTO])
async def create(
    user: UserDTO,
):
    base = BaseController("user")
    hash = get_password_hash(user.password)

    user = UserDBDTO(email=user.email, name=user.username, hashed_password=hash)
    base.create(user)

    return ResponseDTO(data=user)

