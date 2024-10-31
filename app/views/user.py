
from datetime import timedelta
from typing import Annotated, Optional
from app.auth.session import Session, create_session, manager
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordRequestForm,
)

from app.auth.token import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, fake_users_db, get_password_hash
from app.db.models.user import User
from app.dtos.user import Token, UserDTO


user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


auth_scheme = HTTPBearer()

async def get_token(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(auth_scheme),
) -> str:
    # Simulate a database query to find a known token

    if auth is None or manager.validate_token(auth.credentials) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return auth.credentials


@user_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    create_session(access_token, form_data.username)
    print(manager.sessions)
    return Token(access_token=access_token, token_type="bearer")


@user_router.get("/sessions", response_model=list[Session])
async def read_users_me():
    print(manager.sessions)
    return manager.sessions

@user_router.get("/password", response_model=str)
async def password(
    password: str,
):
    return get_password_hash(password)



@user_router.get("/users/me/items/")
async def read_own_items(
    token: HTTPAuthorizationCredentials = Depends(get_token)):
    return [{"item_id": "Foo", "owner": token}]


@user_router.get("/status/")
async def read_system_status(token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)]):
    return {"status": token}


@user_router.post("")
async def create(
    user: UserDTO,
):
    hash = get_password_hash(user.password)
    new_user = User(email=user.email, name=user.username, hashed_password=hash)
    new_user.save()
    return new_user.to_json()