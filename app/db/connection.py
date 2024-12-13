from mongoengine import *

from app.util.config import DB_NAME_KEY

connect(DB_NAME_KEY)