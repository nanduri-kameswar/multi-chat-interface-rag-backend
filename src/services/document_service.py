import asyncio
import uuid

from fastapi import BackgroundTasks, UploadFile
from langchain_core.documents import Document
from langchain_postgres import PGVectorStore
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.exceptions import NotFoundError, ProcessingFailedError
from src.models.document_chunk_model import DocumentChunk
from src.models.document_model import Document as UserDocument
from src.models.enums import DocumentStatus
from src.repositories.document_chunk_repository import DocumentChunkRepository
from src.repositories.document_repository import DocumentRepository
from src.schemas.document_chunk_schema import DocumentChunkResponse
from src.services.conversation_service import ConversationService
from src.utilities.document_utility import add_chunk_metadata
from src.utilities.file_upload_utility import FileParser
from src.utilities.text_splitter_utility import get_text_splitter


class DocumentService:
    def __init__(self, db: AsyncSession, vector_store: PGVectorStore):
        self.repo = DocumentRepository(db)
        self.chunk_repo = DocumentChunkRepository(db, vector_store)
        self.conversation_service = ConversationService(db)
        self.splitter = get_text_splitter()
        self.batch_size = 32

    async def create_document(
        self,
        file: UploadFile,
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
        background_tasks: BackgroundTasks,
    ) -> UserDocument:
        conversation_result = await self.conversation_service.get_conversation(
            conversation_id, user_id
        )
        if not conversation_result:
            raise NotFoundError("Conversation does not exist.")

        parsed_file_docs: list[Document] = await FileParser(file).parse()
        filename = file.filename.lower()
        document = UserDocument(
            user_id=user_id,
            conversation_id=conversation_id,
            file_name=filename,
            status=DocumentStatus.PENDING,
        )
        db_document = await self.repo.create_document(document)

        background_tasks.add_task(
            self.create_document_chunks,
            parsed_file_docs,
            user_id,
            conversation_id,
            db_document.id,
        )

        return db_document

    async def get_document(self, user_id: uuid.UUID, doc_id: uuid.UUID) -> UserDocument:
        return await self.repo.get_document(user_id, doc_id)

    async def get_all_conversation_documents(
        self, user_id: uuid.UUID, convo_id: uuid.UUID
    ) -> list[UserDocument]:
        documents: list[UserDocument] = await self.repo.get_all_conversation_documents(
            user_id, convo_id
        )
        return documents

    async def get_all_user_documents(self, user_id: uuid.UUID) -> list[UserDocument]:
        documents: list[UserDocument] = await self.repo.get_all_user_documents(user_id)
        return documents

    async def delete_document(self, user_id: uuid.UUID, doc_id: uuid.UUID) -> None:
        await self.repo.delete_document(user_id, doc_id)

    async def modify_document_status(
        self, user_id: uuid.UUID, doc_id: uuid.UUID, status: DocumentStatus
    ) -> None:
        await self.repo.modify_document_status(user_id, doc_id, status)

    async def get_all_document_chunks(
        self, user_id: uuid.UUID, doc_id: uuid.UUID
    ) -> list[DocumentChunk]:
        # check this user can access this document or not
        await self.get_document(user_id, doc_id)
        return await self.chunk_repo.get_all_document_chunks(doc_id)

    """
    document chunk creation
    """

    async def create_document_chunks(
        self,
        parsed_file_docs: list[Document],
        user_id: uuid.UUID,
        convo_id: uuid.UUID,
        doc_id: uuid.UUID,
    ):
        await self.repo.modify_document_status(
            user_id, doc_id, DocumentStatus.PROCESSING
        )
        chunked_docs = self.splitter.split_documents(parsed_file_docs)
        chunked_docs_with_metadata = add_chunk_metadata(
            chunked_docs, user_id, convo_id, doc_id
        )
        batches = [
            chunked_docs_with_metadata[i : i + self.batch_size]
            for i in range(0, len(chunked_docs_with_metadata), self.batch_size)
        ]
        tasks = [self.chunk_repo.add_documents(batch) for batch in batches]
        try:
            await asyncio.gather(*tasks)
            await self.repo.modify_document_status(
                user_id, doc_id, DocumentStatus.READY
            )
        except Exception as e:
            await self.repo.modify_document_status(
                user_id, doc_id, DocumentStatus.FAILED
            )
            raise ProcessingFailedError(str(e))

    """
    similarity search for a query text
    """

    async def get_similar_document_chunks(
        self, text: str, user_id: uuid.UUID, convo_id: uuid.UUID, document_id: uuid.UUID
    ) -> list[DocumentChunkResponse]:
        docs = await self.chunk_repo.similarity_search(
            text, user_id, convo_id, document_id
        )
        doc_response = [
            DocumentChunkResponse(
                id=uuid.UUID(doc.id),
                content=doc.page_content,
                source=doc.metadata.get("source", None),
                page=doc.metadata.get("page", None),
            )
            for doc in docs
        ]
        return doc_response
