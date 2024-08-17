from pydantic import BaseModel, field_validator
from fastapi import Body, HTTPException


class PhoneBookRecord(BaseModel):
    phone: str
    address: str

    @classmethod
    def as_form(cls, phone: str = Body(...), address: str = Body(...)):
        return cls(phone, address)
