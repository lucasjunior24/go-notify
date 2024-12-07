from datetime import datetime
from typing import cast
from mongoengine import Document, DateTimeField

class BaseDocument(Document):
    meta = {'allow_inheritance': True, 'abstract': True, 'index_cls': False, 'auto_create_index': False}
    created_at = DateTimeField(default=datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.now(), required=True)


    @classmethod
    def get_by_id(cls, id: str):
        document = cast(cls, cls.objects(id=id).first())
        return document
    
    @classmethod
    def get_all(cls):
        document_list = cast(list[cls], cls.objects())
        return document_list
    
    @classmethod
    def find(cls, key: str, value: str):
        document = cast(cls, cls.objects({key: value}).first())
        return document
    

    @classmethod
    def remove(cls, id: str):
        document = cls.get_by_id(id)
        document.delete()
        return document