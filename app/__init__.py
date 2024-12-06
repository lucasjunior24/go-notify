from fastapi import Header, HTTPException
from app.views.product import product_router
from typing import Annotated
from app.db import connection
from app.views.user import app


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


# app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(product_router)

