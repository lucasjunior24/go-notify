from app.views.product import product_router
from app.views.chat import chat_ai_router
from app.views.session import session_router

from app.views.user import app

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:5173",
]


app.include_router(product_router)
app.include_router(chat_ai_router)
app.include_router(session_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
