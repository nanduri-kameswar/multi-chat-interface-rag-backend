import uuid

from src.models.enums import DocumentStatus
from src.schemas.base_schema import ORMBase

class DocumentResponse(ORMBase):
    id: uuid.UUID
    file_name: str
    status: DocumentStatus
