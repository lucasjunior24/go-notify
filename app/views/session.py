
from datetime import timedelta
from http.client import HTTPException
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.application_manager import ApplicationManager
from app.auth.token import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token
from app.controllers.session import SessionController
from app.dtos.response import ResponseDTO, ResponseModelDTO
from app.dtos.session import SessionDTO
from app.dtos.user import Token


session_router = APIRouter(
    prefix="/session",
    tags=["Session"],
    responses={404: {"description": "Not found"}},
)


@session_router.post("/login")
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
    session_controller = ApplicationManager.get(SessionController)
    session_controller.create(session)
    return Token(access_token=access_token, token_type="bearer")


@session_router.get("/all", response_model=ResponseModelDTO[list[SessionDTO]])
async def read_users_me():
    session_controller = ApplicationManager.get(SessionController)
    all_sessions = session_controller.get_all()
    return ResponseDTO(data=all_sessions, message="success")