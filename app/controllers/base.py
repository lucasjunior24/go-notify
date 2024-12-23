from typing import TypeVar
from bson import ObjectId
from app.db.connection import database
from app.dtos.base import DTO
from app.util.exception import NotFoundedAPI

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


class BaseController[T]:
    def __init__(self, collection: str, dto: T):
        self.collection_name = collection
        self.dto = dto
        self.collection = database[self.collection_name]

    def create(self, dto: type[DTO]):
        dto_json = dto.model_dump(exclude=["id"], mode="json")
        data = self.collection.insert_one(dto_json)
        dto = self.get_by_id(id=data.inserted_id, dto=DTO)
        return dto

    def get_filter(self, key: str, value: str, dto: U | T | None = None):
        data = self.collection.find_one({key: value})
        if dto is None:
            dto = self.dto
        return self.__create_dto(data, dto)

    def get_by_id(self, id: str, dto: U | T | None = None):
        data = self.collection.find_one({"_id": ObjectId(id)})
        if dto is None:
            dto = self.dto
        return self.__create_dto(data, dto)

    def get_with_query(self, data: list[dict], dto: U | T | None = None):
        result_db = list(self.collection.aggregate(data))
        return self.validate_list_dto(result_db, dto)

    def get_all(self, dto: U | T | None = None):
        data = list(self.collection.find())
        return self.validate_list_dto(data, dto)

    def validate_list_dto(self, data: list, dto: U | T | None = None):
        if dto is None:
            dto = self.dto
        result_dto = [self.__create_dto(result, dto) for result in data]
        return result_dto

    @staticmethod
    def __create_dto(data: dict, dto: V) -> V:
        if data is None:
            raise NotFoundedAPI()
        return dto(**data)
