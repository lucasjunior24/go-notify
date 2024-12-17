

from bson import ObjectId
from pydantic import Field

from teste.connnection import database
from teste.dtos.base import DTO


class UserDTO(DTO):
    email: str = Field(default='')
    name: str = Field(default='')
    hashed_password: str = Field(default='')
    disabled: bool = Field(default=False)
    admin: bool = Field(default=False)
    admin_master: bool = Field(default=False)



users_coll = database.get_collection("users")
# userDTO = UserDTO(email="teste", name="lucas")
# user = userDTO.model_dump(exclude=["id"])
# print("userDTO: ", user)
# data = users_coll.insert_one(user)

print()

user = users_coll.find_one({"_id": ObjectId("6760e3238a67621b313794fe")})
print("data: ", user)
# userDTO = UserDTO(**user)
# print()
# print("userDTO: ", userDTO)