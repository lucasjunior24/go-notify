from mongoengine import *

from app.util.config import DB_NAME_KEY


host = "mongodb://localhost:27017/lucas_teste"
# connect(db=None, alias=DEFAULT_CONNECTION_NAME )
connect(DB_NAME_KEY)