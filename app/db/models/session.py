from datetime import datetime
from typing import cast
from mongoengine import *

class Session(Document):
    token = StringField(required=True)
    user_id = StringField(max_length=50, required=True)
    user_name = StringField(max_length=100, required=True)
    created_at = DateTimeField(default=datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.now(), required=True)
    expires_at = DateTimeField(default=datetime.now(), required=True)

    def to_json(self):
        return {
            "id": str(self.pk),
            "token": self.token,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "expires_at": str(self.expires_at),
        }
    
    @classmethod
    def get_session_by_user_id(cls, user_id: str):
        session = cast(Session, cls.objects(user_id=user_id).first())
        return session

    @classmethod
    def create(cls, token: str, user_id: str,user_name: str, expires_at=datetime):
        session = Session(token=token, user_id=user_id,user_name=user_name, expires_at=expires_at)
        session.save()
        return session

    
    @classmethod
    def get_session_by_token(cls, token: str):
        session = cast(Session, cls.objects(token=token).first())
        return session
    

    @staticmethod
    def session_expired(token: str) -> bool:
        type, token = token.split(" ")
        session = Session.get_session_by_token(token)
        now = datetime.now()
        expire = bool(session.expires_at <= now)

        return expire
