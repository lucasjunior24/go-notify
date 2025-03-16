from typing import Optional, TypeVar

from mongomock import MongoClient

from app.controllers.base import BaseController


GenericController = TypeVar("GenericController")


class ApplicationManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApplicationManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.control = {}

    @staticmethod
    def get(
        controller: type[GenericController], client: Optional[MongoClient] = None
    ) -> GenericController:
        application = ApplicationManager()
        return application.create_instance(controller, client)

    def create_instance(
        self, controller: BaseController, _client: Optional[MongoClient]
    ):
        if self.control.get(controller.collection_name) is None:
            self.control[controller.collection_name] = controller(_client=_client)
        return self.control[controller.collection_name]
