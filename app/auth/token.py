from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Protocol
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from passlib.context import CryptContext
from pymongo import MongoClient
from app.application_manager import ApplicationManager
from app.controllers.session import SessionController

from app.controllers.user import UserController
from app.db.models.user import UserDTO
from basic_components_fpp.exception import UnauthorizedAPI


class AccessTokenBearer(HTTPBearer):
    pass


SECRET_KEY = "45debe25ff6e17a8bed5b867df33183a3b44c280ef5177b51677e48866a23816"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_scheme = HTTPBearer()


class ValidateToken(Protocol):
    def __init__(
        self,
        auth: Optional[HTTPAuthorizationCredentials] = Depends(auth_scheme),
    ) -> str:

        # Simulate a database query to find a known token
        self.auth = auth
        self.sessionController = ApplicationManager.get(SessionController)

    def __str__(self):
        if self.auth is None or self.sessionController.session_expired(
            token=self.auth.credentials
        ):
            raise UnauthorizedAPI()
        return self.auth.credentials


def get_token(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(auth_scheme),
) -> str:
    # Simulate a database query to find a known token
    sessionController = ApplicationManager.get(SessionController)
    if auth is None or sessionController.session_expired(token=auth.credentials):
        raise UnauthorizedAPI()
    return auth.credentials


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(email: str, password: str):
    user_controller = ApplicationManager.get(UserController)
    user = user_controller.get_filter("email", email, UserDTO)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
