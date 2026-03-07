from pymongo import MongoClient
from app.controllers.base import BaseController
from app.db.models.product import ProductDTO


class ProductController(BaseController[ProductDTO]):
    collection_name = "product"

    def __init__(
        self, dto: ProductDTO = ProductDTO, _client: MongoClient | None = None
    ):
        super().__init__(dto, _client)
