import uuid
from datetime import datetime, timezone

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.exceptions import (ConflictError, ForbiddenError,
                                            NotFoundError)
from src.models import Conversation
from src.schemas.conversation_schema import ConversationUpdate


class ConversationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_conversation(self, conversation: Conversation) -> Conversation:
        result = await self.db.execute(
            select(Conversation).where(
                and_(
                    Conversation.user_id == conversation.user_id,
                    Conversation.title == conversation.title,
                )
            )
        )
        matching_convo: Conversation | None = result.scalar_one_or_none()
        if matching_convo:
            raise ConflictError(
                "Document with same name already exists in the conversation"
            )
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation

    async def get_conversation(
        self, conversation_id: uuid.UUID, user_id: uuid.UUID
    ) -> Conversation:
        result = await self.db.execute(
            select(Conversation).where(
                and_(
                    Conversation.id == conversation_id, Conversation.user_id == user_id
                )
            )
        )
        conversation: Conversation | None = result.scalar_one_or_none()
        if not conversation:
            raise NotFoundError("Conversation not found")
        return conversation

    async def get_all_conversations(self, user_id: uuid.UUID) -> list[Conversation]:
        result = await self.db.execute(
            select(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )
        conversations: list[Conversation] = list(result.scalars().all())
        return conversations

    async def update_conversation(
        self,
        updated_conversation: ConversationUpdate,
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Conversation:
        result = await self.db.execute(
            select(Conversation).where(
                and_(
                    Conversation.user_id == user_id,
                    Conversation.title == updated_conversation.title,
                )
            )
        )
        matching_convo_title: Conversation | None = result.scalar_one_or_none()
        if matching_convo_title:
            raise ConflictError(
                "Document with same name already exists in the conversation"
            )
        db_conversation = await self.get_conversation(conversation_id, user_id)
        db_conversation.title = updated_conversation.title
        db_conversation.updated_at = datetime.now(timezone.utc)
        await self.db.commit()
        return db_conversation

    async def delete_conversation(
        self, conversation_id: uuid.UUID, user_id: uuid.UUID
    ) -> Conversation:
        conversation: Conversation | None = await self.get_conversation(
            conversation_id, user_id
        )
        if not conversation:
            raise NotFoundError("Conversation not found")
        await self.db.delete(conversation)
        await self.db.commit()
        return conversation
