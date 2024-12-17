
from datetime import datetime
from typing import Optional, Annotated
from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, WithJsonSchema, Field, PlainSerializer


def to_object_id(value):
    if isinstance(value, str):
        return ObjectId(value)
    return value


def to_str(value):
    return str(value)


CustomObjectId = Annotated[ObjectId, BeforeValidator(to_object_id), PlainSerializer(to_str, str, "json"), WithJsonSchema({"type": "string"}, mode='validation')]

class BaseDTO(BaseModel):
    ...

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, use_enum_values=True)



class DTO(BaseDTO):
    id: Optional[CustomObjectId] = Field(alias='_id', default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    updated_by: str = Field(default='')
    created_by: str = Field(default='')

