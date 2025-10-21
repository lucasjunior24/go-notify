from typing import Optional, TypeVar
from bson import ObjectId
from mongomock import MongoClient
from app.dtos.base import DTO
from app.util.config import DB_NAME
from basic_components_fpp.exception import NotFoundAPI


T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
from app.db.connection import client


class BaseController[T]:
    collection_name: str

    def __init__(self, dto: T, _client: Optional[MongoClient] | None = None):
        self.client = client if _client is None else _client
        database = self.client.get_database(DB_NAME)
        self.dto = dto

        self.collection = database[self.collection_name]

    def create(self, data: DTO):
        dto_json = data.model_dump(exclude=["id"], mode="json")
        data = self.collection.insert_one(dto_json)
        new_dto = self.get_by_id(id=data.inserted_id, dto=self.dto)
        return new_dto

    def get_filter(self, key: str, value: str, dto: U | T | None = None) -> U | T:
        data = self.collection.find_one({key: value})
        if dto is None:
            dto = self.dto
        return self.__create_dto(data, dto)

    def get_by_id(self, id: str, dto: U | T | None = None):
        data = self.collection.find_one({"_id": ObjectId(id)})
        if dto is None:
            dto = self.dto
        return self.__create_dto(data, dto)

    def get_with_query(
        self, data: list[dict], dto: type[U] | T | None = None
    ) -> list[U | T]:
        result_db = list(self.collection.aggregate(data))
        return self.validate_list_dto(result_db, dto)

    def get_all(self, dto: type[U] | T | None = None) -> list[U | T]:
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
            raise NotFoundAPI()
        return dto(**data)
