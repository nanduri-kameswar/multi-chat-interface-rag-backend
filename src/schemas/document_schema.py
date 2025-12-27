import uuid

from pydantic import BaseModel

from src.models.enums import DocumentStatus
from src.schemas.base_schema import ORMBase


class DocumentCreate(BaseModel):
    file_name: str
    conversation_id: uuid.UUID


class DocumentResponse(ORMBase):
    id: uuid.UUID
    file_name: str
    status: DocumentStatus
