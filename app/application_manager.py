from typing import TypeVar, Generic

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
    def get(controller: type[GenericController]) -> GenericController:
        apliication = ApplicationManager()
        return apliication.create_instance(controller)

    def create_instance(self, controller: BaseController):
        if self.control.get(controller.collection_name) is None:
            self.control[controller.collection_name] = controller()
        return self.control[controller.collection_name]
