from mongoengine import *

from app.util.config import DB_URL, DB_NAME_KEY


print("")
print("")
print(DB_NAME_KEY)
print("")
print("")

connect(DB_NAME_KEY, host=DB_URL)