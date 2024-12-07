from datetime import datetime
from typing import cast
from mongoengine import *

class Product(Document):
    price = StringField(required=True)
    name = StringField(max_length=50, required=True)
    description = StringField(max_length=100, required=True)
    created_at = DateTimeField(default=datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.now(), required=True)

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
    
    @classmethod
    def get_by_id(cls, product_id: str):
        product = cast(Product, cls.objects(id=product_id).first())
        return product
    
    @classmethod
    def get_all(cls):
        product_list = cast(list[Product], cls.objects())
        return product_list
    

    @classmethod
    def remove(cls, product_id: str):
        product = cls.get_by_id(product_id)
        product.delete()
        return product