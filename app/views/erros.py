
from http import HTTPStatus
from app.dtos.response import ResponseDTO
from app.util.exception import ExceptionAPI, IExceptionAPI,UnauthorizedAPI
from fastapi.encoders import jsonable_encoder
from app.views import app
from fastapi import Request, Response
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(IExceptionAPI)
async def exception_handler(request: Request, exc: IExceptionAPI):
    message = exc.message if exc.message else HTTPStatus(exc.status_code).description
    response = ResponseDTO(message=message, status=exc.status, data=None)
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(response),
    )


