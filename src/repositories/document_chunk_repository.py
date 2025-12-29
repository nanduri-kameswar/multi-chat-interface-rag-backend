import uuid

from langchain_core.documents import Document
from langchain_postgres import PGVectorStore
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.exceptions.exceptions import ProcessingFailedError
from src.models.document_chunk_model import DocumentChunk


class DocumentChunkRepository:
    def __init__(self, db: AsyncSession, vector_store: PGVectorStore):
        self.db = db
        self.vector_store = vector_store

    """
    adding document chunks into pgvector database
    """

    async def add_documents(self, chunks: list[Document]):
        try:
            await self.vector_store.aadd_documents(chunks)
        except Exception as e:
            raise ProcessingFailedError(str(e))

    """
    similarity search of a text from pgvector database
    """

    async def similarity_search(
        self, text: str, user_id: uuid.UUID, conversation_id: uuid.UUID, document_id: uuid.UUID
    ) -> list[Document]:
        docs = await self.vector_store.asimilarity_search(
            text,
            k=settings.SIMILARITY_SEARCH_K,
            filter={
                "document_id": str(document_id)
            },
        )
        return docs

    async def get_all_document_chunks(
        self, document_id: uuid.UUID
    ) -> list[DocumentChunk]:
        result = await self.db.execute(
            select(DocumentChunk).where(DocumentChunk.document_id == document_id)
        )
        document_chunks: list[DocumentChunk] = result.scalars().all()
        return document_chunks
