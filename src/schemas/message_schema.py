import uuid
from datetime import datetime

from pydantic import BaseModel

from src.models.enums import MessageRole
from src.schemas.base_schema import ORMBase


class MessageCreate(BaseModel):
    conversation_id: uuid.UUID
    role: MessageRole
    content: str


class MessageResponse(ORMBase):
    role: str
    content: str
    created_at: datetime
