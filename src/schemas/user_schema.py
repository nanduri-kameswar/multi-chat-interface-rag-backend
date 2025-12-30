from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator, Field

from src.models.enums import UserRole
from src.schemas.base_schema import ORMBase
import re

class UserCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="User full name"
    )
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        description="Password must contain upper, lower, digit, and special char"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.replace(" ", "").isalpha():
            raise ValueError("Name must contain only alphabets and spaces")
        return v.strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        _validate_password_strength(v)
        return v


class UserUpdate(BaseModel):
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        _validate_password_strength(v)
        return v


class UserResponse(ORMBase):
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime


def _validate_password_strength(password: str) -> None:
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain at least one special character")