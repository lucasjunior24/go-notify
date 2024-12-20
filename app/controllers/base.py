

from typing import TypeVar
from bson import ObjectId
from app.db.connection import database
from app.dtos.base import DTO

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


class BaseController[T]:
  def __init__(self, collection: str, dto: T):
    self.collection_name = collection
    self.dto = dto
    self.collection = database[self.collection_name]


  def create(self, dto: type[DTO]):
    dto_json = dto.model_dump(exclude=["id"], mode='json')
    data = self.collection.insert_one(dto_json)
    dto = self.get_by_id(id=data.inserted_id, dto=DTO)
    return dto

  def get_filter(self, key: str, value: str, dto: U | None = None):
    data = self.collection.find_one({key: value})
    if dto:
      return self.__create_dto(data, dto)
    return self.__create_dto(data, self.dto)
  

  def get_by_id(self, id: str, dto: U | None = None):
    data = self.collection.find_one({"_id": ObjectId(id)})
    if dto:
      return self.__create_dto(data, dto)
    return self.__create_dto(data, self.dto)
  
  def get_with_query(self, data: list[dict], dto: U | None = None):
    result_db = list(self.collection.aggregate(data))
    if dto:
      result_dto = [self.__create_dto(result, dto) for result in result_db]
      return result_dto
    result_dto = [self.__create_dto(result, self.dto) for result in result_db]
    return result_dto
  
  @staticmethod
  def __create_dto(data: dict, dto: V) -> V:
    return dto(**data)