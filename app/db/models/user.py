from typing import cast
from bson import ObjectId
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
    def get_user_with_sessions(cls, user_id: str):
        users_db = list(cls.objects().aggregate([ { "$addFields": { "id": "$_id" } },{'$match' : { "id" : ObjectId(user_id) }}, {
        '$lookup':
            {
                'from': 'session',
                'localField':'user_id',
                'foreignField': 'id',
                'as': 'session'
            }
        }]))
        users = [User(**user) for user in users_db]
        return users
    