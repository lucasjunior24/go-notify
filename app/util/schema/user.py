from marshmallow_mongoengine import ModelSchema

from app.db.models.user import User



class UserSchema(ModelSchema):
    class Meta:
        model = User

user_schema: UserSchema = UserSchema()

