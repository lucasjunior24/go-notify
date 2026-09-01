from http import HTTPStatus
import app
from app.dtos.response import ResponseDTO

from fastapi.encoders import jsonable_encoder

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def midle_erros(app: FastAPI):
    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        if exc.args:
            message = exc.args[0]
            status = "Internal Server Error"
            status_code = 500
        else:
            message = (
                exc.message if exc.message else HTTPStatus(exc.status_code).description
            )
            status = exc.status
            status_code = exc.status_code
        response = ResponseDTO(message=message, status=status, data=None)
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(response),
        )
