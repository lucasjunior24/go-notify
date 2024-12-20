
from bson import ObjectId
from app.controllers.base import BaseController
from app.dtos.user import UserDBDTO, UserDBSessionDTO

class UserController(BaseController[UserDBDTO]):
  def __init__(self, collection  = "user", dto: UserDBDTO = UserDBDTO):
    super().__init__(collection, dto)


  def get_user_with_sessions(self, user_id: str):
      query = [ { "$addFields": { "id": "$_id" } },{'$match' : { "id" : ObjectId(user_id) }}, {
      '$lookup':
          {
              'from': 'session',
              'localField':'user_id',
              'foreignField': 'id',
              'as': 'session'
          }
      }]
      users = self.get_with_query(data=query, dto=UserDBSessionDTO)
      return users