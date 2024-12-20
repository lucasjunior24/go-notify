from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from passlib.context import CryptContext

from app.controllers.session import SessionController
from app.controllers.user import UserController
from app.db.models.session import Session
from app.db.models.user import User
from app.dtos.user import UserDBDTO
from app.util.exception import UnauthorizedAPI

class AccessTokenBearer(HTTPBearer):
  pass

SECRET_KEY = "45debe25ff6e17a8bed5b867df33183a3b44c280ef5177b51677e48866a23816"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_scheme = HTTPBearer()


async def get_token(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(auth_scheme),
) -> str:
    # Simulate a database query to find a known token
    controller = SessionController()
    if auth is None or controller.session_expired(token=auth.credentials):
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
    base = UserController()

    user = base.get_filter('email', email, UserDBDTO)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


