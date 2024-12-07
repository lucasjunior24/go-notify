from datetime import datetime
from typing import cast
from mongoengine import *

from app.db.models.base import BaseDocument

class Product(BaseDocument):
    price = StringField(required=True)
    name = StringField(max_length=50, required=True)
    description = StringField(max_length=100, required=True)

    def to_json(self):
        return {
            "id": str(self.pk),
            "price": self.price,
            "name": self.name,
            "description": self.description,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
    
    @classmethod
    def get_product_by_email(cls, email: str):
        doctor = cast(Product, cls.objects(email=email).first())
        return doctor
