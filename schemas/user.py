import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, constr


class UserBaseSchema(BaseModel):
    email: EmailStr | None = None
    phone_number: str
    full_name: str | None = None


class UserUpdateSchema(UserBaseSchema):
    password: constr(min_length=8) | None = None


class UserSchema(UserBaseSchema):
    id: uuid.UUID
    is_active: bool
    is_staff: bool
    is_superuser: bool
    joined_date: datetime

    class Config:
        orm_mode = True
