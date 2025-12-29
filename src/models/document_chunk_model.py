import uuid
from typing import Any

from pgvector.sqlalchemy import VECTOR
from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.config import settings
from src.db.connection import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        index=True,
    )
    content: Mapped[str] = mapped_column(Text)

    embedding: Mapped[list[float]] = mapped_column(
        VECTOR(settings.VECTOR_SIZE), nullable=False, default=[]
    )

    cmetadata: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    document = relationship("Document", back_populates="chunks")
