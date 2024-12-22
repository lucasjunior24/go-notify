
from bson import ObjectId
from app.controllers.base import BaseController
from app.db.models.user import UserDTO
from app.dtos.user import UserDBSessionDTO

class UserController(BaseController[UserDTO]):
  def __init__(self, collection  = "user", dto: UserDTO = UserDTO):
    super().__init__(collection, dto)


  def get_user_with_sessions(self, user_id: str):
      query = [ { "$addFields": { "id": "$_id" } },{'$match' : { "id" : ObjectId(user_id) }}, {
      '$lookup':
          {
              'from': 'session',
              'localField':'id',
              'foreignField': 'user_id',
              'as': 'session'
          }
      }]
      users = self.get_with_query(data=query, dto=UserDBSessionDTO)
      return users
  


userController = UserController()