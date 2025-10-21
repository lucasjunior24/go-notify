from basic_components_fpp.exception import IExceptionAPI
from http import HTTPStatus


class NewTestAPI(IExceptionAPI):
    data: str | None = None
    message: str = HTTPStatus(450).description
    status: str = HTTPStatus(450).phrase
    status_code: int = 450
