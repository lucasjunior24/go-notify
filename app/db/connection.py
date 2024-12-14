from mongoengine import *

from app.util.config import DB_URL, DB_NAME


connect(DB_NAME, host=DB_URL)