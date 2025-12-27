import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr

from src.models.enums import UserRole
from src.schemas.base_schema import ORMBase


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    current_password: str
    new_password: str


class UserResponse(ORMBase):
    id: uuid.UUID
    email: EmailStr
    role: UserRole
    created_at: datetime
