
from http import HTTPStatus
from app.util.exception import ExceptionAPI
from app.views import app
from fastapi import Request, Response
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(ExceptionAPI)
async def unicorn_exception_handler(request: Request, exc: ExceptionAPI):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message if exc.message else HTTPStatus(exc.status_code).phrase, "status": HTTPStatus(exc.status_code).phrase},
    )


