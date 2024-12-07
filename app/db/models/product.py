
from mongoengine import *

from app.db.models.base import BaseDocument
from app.db.models.reviews import Review

class Product(BaseDocument):
    price = StringField(required=True)
    name = StringField(max_length=50, required=True)
    description = StringField(max_length=100, required=True)

    reviews = ListField(EmbeddedDocumentField(Review), default=[])