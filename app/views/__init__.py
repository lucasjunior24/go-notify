from fastapi import FastAPI

from app.views.erros import midle_erros

app = FastAPI(
    description="Application for managing users, sessions, products, and chat AI interactions."
)
midle_erros(app=app)
