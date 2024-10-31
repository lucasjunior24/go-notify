from datetime import datetime
from typing import cast
from mongoengine import *

class Doctor(Document):
    email = StringField(required=True)
    name = StringField(max_length=50, required=True)
    specialization = StringField(max_length=100, required=True)
    clinic = StringField(max_length=50, required=True)
    address = StringField(max_length=80)
    phone_number = IntField(max_length=12)
    created_at = DateTimeField(default=datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.now(), required=True)

    def to_json(self):
        return {
            "id": str(self.pk),
            "email": self.email,
            "name": self.name,
            "specialization": self.specialization,
            "address": self.address,
            "clinic": self.clinic,
            "phone_number": self.phone_number,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
    
    @classmethod
    def get_doctor_by_email(cls, email: str):
        doctor = cast(Doctor, cls.objects(email=email).first())
        return doctor