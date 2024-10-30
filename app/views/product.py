from fastapi import APIRouter

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/product",
    tags=["product"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
@router.get("/")
async def get_all():
    return {"message": "Product"}

