import uuid
from datetime import datetime

from pydantic import BaseModel

from src.schemas.base_schema import ORMBase


class ConversationCreate(BaseModel):
    title: str


class ConversationUpdate(ConversationCreate):
    pass


class ConversationResponse(ORMBase):
    id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
