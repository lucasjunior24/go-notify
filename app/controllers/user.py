
from app.controllers.base import BaseController

class UserController(BaseController):
  def __init__(self, collection = "user"):
    super().__init__(collection)
