

from typing import Type, TypeVar
from bson import ObjectId
from pymongo import MongoClient

from teste.dtos.base import DTO
from teste.config import IP_WITH_PORT_DB
from teste.connnection import database

T = TypeVar("T")
class BaseController:
  def __init__(self, collection: str):
    self.collection_name = collection
    self.client = MongoClient(f"mongodb://{IP_WITH_PORT_DB}")
    self.collection = database[self.collection_name]



  def create(self, dto: type[DTO]):
    dto_json = dto.model_dump(exclude=["id"], mode='json')
    print(dto_json)
    self.collection.insert_one(dto_json)




  def get_by_id(self, id: str, dto: Type[T]) -> Type[T]:
    data = self.collection.find_one({"_id": ObjectId(id)})
    return self.__create_dto(data, dto)
  
  @staticmethod
  def __create_dto(data: dict, dto: Type[T]) -> Type[T]:
    return dto(**data)