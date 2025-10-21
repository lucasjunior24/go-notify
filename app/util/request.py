from typing import TypeVar
import requests


from basic_components_fpp.exception import ExceptionAPI

T = TypeVar("T")


class Request:
    def __init__(self, url: str):
        self.url = url

    def post(self, params: dict, route: str, dto: type[T]) -> T:
        response = requests.post(url=self.url + route, params=params)
        if not response.ok:
            raise ExceptionAPI()
        result = response.json()
        return result["data"]
