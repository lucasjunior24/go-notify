
from datetime import datetime
from typing import Optional, Annotated
from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, WithJsonSchema, Field, PlainSerializer

from app.util.config import IP_WITH_PORT_DB

def to_object_id(value):
    if isinstance(value, str):
        return ObjectId(value)
    return value


def to_str(value):
    return str(value)


CustomObjectId = Annotated[ObjectId, BeforeValidator(to_object_id), PlainSerializer(to_str, str, "json"), WithJsonSchema({"type": "string"}, mode='validation')]

class BaseDTO(BaseModel):
    ...

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, use_enum_values=True)



class DTO(BaseDTO):
    
    id: Optional[CustomObjectId] = Field(alias='_id', default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    updated_by: str = Field(default='')
    created_by: str = Field(default='')


class UserDTO(DTO):
    email: str = Field(default='')
    name: str = Field(default='')
    hashed_password: str = Field(default='')
    disabled: bool = Field(default=False)
    admin: bool = Field(default=False)
    admin_master: bool = Field(default=False)


from pymongo import MongoClient


client = MongoClient(f"mongodb://{IP_WITH_PORT_DB}")


database = client.get_database("teste")

users_coll = database.get_collection("users")
# userDTO = UserDTO(email="teste", name="lucas")
# user = userDTO.model_dump(exclude=["id"])
# print("userDTO: ", user)
# data = users_coll.insert_one(user)

print()

user = users_coll.find_one({"_id": ObjectId("6760e3238a67621b313794fe")})
print("data: ", user)
userDTO = UserDTO(**user)
print()
print("userDTO: ", userDTO)