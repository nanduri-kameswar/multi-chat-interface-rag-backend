import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from src.schemas.base_schema import ORMBase


class MessageCreate(BaseModel):
    conversation_id: uuid.UUID
    role: Literal["system", "assistant", "user"]
    content: str


class MessageResponse(ORMBase):
    role: str
    content: str
    created_at: datetime
