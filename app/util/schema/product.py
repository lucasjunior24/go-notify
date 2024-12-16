from marshmallow_mongoengine import ModelSchema

from app.db.models.product import Product

class ProductSchema(ModelSchema):
    class Meta:
        model = Product



product_schema: ProductSchema = ProductSchema()