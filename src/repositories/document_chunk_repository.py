import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.document_chunk_model import DocumentChunk


class DocumentChunkRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_document_chunks(self, chunks: list[DocumentChunk]):
        self.db.add(chunks)
        await self.db.commit()
        await self.db.refresh(chunks)

    async def get_all_document_chunks(
        self, document_id: uuid.UUID
    ) -> list[DocumentChunk]:
        result = await self.db.execute(
            select(DocumentChunk).where(DocumentChunk.id == document_id)
        )
        document_chunks: list[DocumentChunk] = list(result.scalars())
        return document_chunks
