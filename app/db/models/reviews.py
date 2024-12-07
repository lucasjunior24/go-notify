
from mongoengine import *


class Review(EmbeddedDocument):
    score = StringField(required=True)
    comment = StringField(max_length=50, required=True)
    photo = StringField(max_length=100, required=True)
    
