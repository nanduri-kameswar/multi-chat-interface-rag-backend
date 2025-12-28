import uuid

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.exceptions import NotFoundError, ProcessingFailedError
from src.embeddings.factory import get_embedding_provider
from src.models.document_chunk_model import DocumentChunk
from src.models.document_model import Document
from src.models.enums import DocumentStatus
from src.repositories.document_chunk_repository import DocumentChunkRepository
from src.repositories.document_repository import DocumentRepository
from src.services.conversation_service import ConversationService
from src.utilities.document_utility import create_chunks_from


class DocumentService:
    def __init__(self, db: AsyncSession):
        self.repo = DocumentRepository(db)
        self.chunk_repo = DocumentChunkRepository(db)
        self.conversation_service = ConversationService(db)
        self.embedder = get_embedding_provider()

    async def create_document(
        self,
        file_name: str,
        conversation_id: uuid.UUID,
        text: str,
        user_id: uuid.UUID,
        background_tasks: BackgroundTasks,
    ) -> Document:
        conversation_result = await self.conversation_service.get_conversation(
            conversation_id, user_id
        )
        if not conversation_result:
            raise NotFoundError("Conversation does not exist.")
        document = Document(
            user_id=user_id,
            conversation_id=conversation_id,
            file_name=file_name,
            status=DocumentStatus.PENDING,
        )
        db_document = await self.repo.create_document(document)
        background_tasks.add_task(
            self.create_document_chunks, user_id, db_document.id, text
        )
        return db_document

    async def get_document(self, user_id: uuid.UUID, doc_id: uuid.UUID) -> Document:
        return await self.repo.get_document(user_id, doc_id)

    async def get_all_conversation_documents(
        self, user_id: uuid.UUID, convo_id: uuid.UUID
    ) -> list[Document]:
        documents: list[Document] = await self.repo.get_all_conversation_documents(
            user_id, convo_id
        )
        return documents

    async def get_all_user_documents(self, user_id: uuid.UUID) -> list[Document]:
        documents: list[Document] = await self.repo.get_all_user_documents(user_id)
        return documents

    async def delete_document(self, user_id: uuid.UUID, doc_id: uuid.UUID) -> None:
        await self.repo.delete_document(user_id, doc_id)

    async def modify_document_status(
        self, user_id: uuid.UUID, doc_id: uuid.UUID, status: DocumentStatus
    ) -> None:
        await self.repo.modify_document_status(user_id, doc_id, status)

    async def create_document_chunks(
        self, user_id: uuid.UUID, doc_id: uuid.UUID, text: str
    ):
        await self.modify_document_status(user_id, doc_id, DocumentStatus.PROCESSING)
        try:
            text_chunks: list[str] = create_chunks_from(text)
            embeddings = self.embedder().embed(text_chunks)
            chunk_objs = [
                DocumentChunk(document_id=doc_id, content=text, embedding=vector)
                for text, vector in zip(text_chunks, embeddings)
            ]
            await self.chunk_repo.create_document_chunks(chunk_objs)
            await self.modify_document_status(user_id, doc_id, DocumentStatus.READY)
        except Exception as e:
            await self.modify_document_status(user_id, doc_id, DocumentStatus.FAILED)
            raise ProcessingFailedError(str(e))

    async def get_all_document_chunks(
        self, user_id: uuid.UUID, doc_id: uuid.UUID
    ) -> list[DocumentChunk]:
        # check this user can access this document or not
        await self.get_document(user_id, doc_id)
        return await self.chunk_repo.get_all_document_chunks(doc_id)
