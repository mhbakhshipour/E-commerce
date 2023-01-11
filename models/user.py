import uuid
import datetime

from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from restaurant_crm.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String(65), index=True, nullable=True)
    phone_number = Column(String(15), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    joined_date = Column(DateTime, default=datetime.datetime.utcnow)


"""
    For create migration please run this command:
    poetry run alembic revision --autogenerate -m "COMMENT"
"""
