import uuid

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.exceptions import ConflictError, ForbiddenError, NotFoundError
from src.models.document_model import Document
from src.models.enums import DocumentStatus


class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_document(self, document: Document) -> Document:
        # if any document name matches then raise conflict error
        result = await self.db.execute(
            select(Document).where(
                and_(
                    Document.conversation_id == document.conversation_id,
                    Document.file_name == document.file_name,
                )
            )
        )
        matching_document: Document | None = result.scalar_one_or_none()
        if matching_document:
            raise ConflictError(
                "Document with same name already exists in the conversation"
            )
        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)
        return document

    async def get_document(self, user_id: uuid.UUID, doc_id: uuid.UUID) -> Document:
        result: Document | None = await self.db.get(Document, doc_id)
        if not result:
            raise NotFoundError("Document not found")
        elif result.user_id != user_id:
            raise ForbiddenError("User is not allowed to read document")
        return result

    async def get_all_conversation_documents(
        self, user_id: uuid.UUID, convo_id: uuid.UUID
    ) -> list[Document]:
        result = await self.db.execute(
            select(Document).where(
                and_(Document.conversation_id == convo_id, Document.user_id == user_id)
            )
        )
        documents: list[Document] = result.scalars().all()
        return documents

    async def get_all_user_documents(self, user_id: uuid.UUID) -> list[Document]:
        result = await self.db.execute(
            select(Document).where(Document.user_id == user_id)
        )
        documents: list[Document] = result.scalars().all()
        return documents

    async def delete_document(self, user_id: uuid.UUID, doc_id: uuid.UUID) -> None:
        doc = await self.get_document(user_id, doc_id)
        if doc and doc.user_id == user_id:
            await self.db.delete(doc)
            await self.db.commit()
        else:
            raise ForbiddenError("User is not authorized to delete this document")

    async def modify_document_status(
        self, user_id: uuid.UUID, doc_id: uuid.UUID, status: DocumentStatus
    ) -> None:
        doc = await self.get_document(user_id, doc_id)
        if doc and doc.user_id == user_id:
            doc.status = status
            await self.db.commit()
        else:
            raise ForbiddenError("User is not authorized to modify this document")
