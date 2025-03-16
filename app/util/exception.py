from dataclasses import dataclass
from http import HTTPStatus


@dataclass
class IExceptionAPI(Exception): ...


class ExceptionAPI(IExceptionAPI):
    data: str | None = None
    message: str = HTTPStatus(500).description
    status: str = HTTPStatus(500).phrase
    status_code: int = 500


class UnauthorizedAPI(IExceptionAPI):
    data: str | None = None
    message: str = HTTPStatus(401).description
    status: str = HTTPStatus(401).phrase
    status_code: int = 401


class NotFoundAPI(IExceptionAPI):
    data: str | None = None
    message: str = HTTPStatus(404).description
    status: str = HTTPStatus(404).phrase
    status_code: int = 404
