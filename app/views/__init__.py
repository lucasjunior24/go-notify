from fastapi import FastAPI

from app.db import connection
app = FastAPI(description="test")
