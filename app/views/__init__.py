from fastapi import FastAPI

from app.views.erros import midle_erros

app = FastAPI(description="test")
midle_erros(app=app)
