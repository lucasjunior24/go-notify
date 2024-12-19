
from app.controllers.base import BaseController

class ProductController(BaseController):
  def __init__(self, collection = "product"):
    super().__init__(collection)
