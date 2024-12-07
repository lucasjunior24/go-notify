from marshmallow_mongoengine import ModelSchema

from app.db.models.product import Product
from app.db.models.user import User

class ProductSchema(ModelSchema):
    class Meta:
        model = Product

class UserSchema(ModelSchema):
    class Meta:
        model = User

product_schema: ProductSchema = ProductSchema()