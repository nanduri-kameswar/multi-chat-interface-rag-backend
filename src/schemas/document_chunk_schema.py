import uuid

from src.schemas.base_schema import ORMBase


class DocumentChunkResponse(ORMBase):
    id: uuid.UUID
    content: str
    source: str
