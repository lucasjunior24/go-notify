from datetime import datetime, timedelta, timezone

from app.auth.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.dtos.session import SessionDTO


ACCESS_TOKEN_EXPIRES = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
TOKEN_TEST, expire = create_access_token(
    data={"sub": "lucas", "scopes": ""},
    expires_delta=ACCESS_TOKEN_EXPIRES,
)
BEARER_TOKEN_TEST = f"Bearer {TOKEN_TEST}"

SESSION_DTO_TEST = SessionDTO(
    token=TOKEN_TEST,
    expires_at=datetime.now(timezone.utc),
    user_name="lucas",
    user_id="",
)
