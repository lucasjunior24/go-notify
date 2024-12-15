from datetime import datetime
from typing import cast
from mongoengine import *

from app.db.models.base import BaseDocument
from app.util.exception import ExceptionAPI, UnauthorizedAPI

class User(BaseDocument):
    email = StringField(required=True)
    name = StringField(max_length=50)
    hashed_password = StringField(max_length=100)
    disabled = BooleanField(default=False)
    admin = BooleanField(default=False)
    admin_master = BooleanField(default=False)

    def to_json(self):
        return {
            "id": str(self.pk),
            "email": self.email,
            "name": self.name,
            "hashed_password": self.hashed_password,
            "disabled": self.disabled,
            "admin": self.admin,
            "admin_master": self.admin_master,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
    
    @classmethod
    def get_user_by_email(cls, email: str):
        user = cast(User, cls.objects(email=email).first())
        if user is None:
            raise ExceptionAPI()
        return user
    
