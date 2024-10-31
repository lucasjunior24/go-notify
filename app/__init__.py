from fastapi import Depends, Header, HTTPException, FastAPI
from app.views.product import router
from app.views.user import user_router
from typing import Annotated

async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

app.include_router(router)
app.include_router(user_router)

