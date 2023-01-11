import re

from pydantic import BaseModel, constr, validator


class UserLoginSchema(BaseModel):
    phone_number: str
    password: str


class UserCreateSchema(BaseModel):
    phone_number: str
    password: constr(min_length=8)

    @validator("phone_number")
    def phone_number_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v
