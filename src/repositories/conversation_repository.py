import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.exceptions import ForbiddenError, NotFoundError
from src.models import Conversation
from src.schemas.conversation_schema import ConversationUpdate


class ConversationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_conversation(self, conversation: Conversation) -> Conversation:
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation

    async def get_conversation(
        self, conversation_id: uuid.UUID, user_id: uuid.UUID
    ) -> Conversation:
        result = await self.db.execute(
            select(Conversation).filter(Conversation.id == conversation_id)
        )
        conversation: Conversation | None = result.scalar_one_or_none()
        if not conversation:
            raise NotFoundError("Conversation not found")
        if conversation.user_id != user_id:
            raise ForbiddenError("Access denied")
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
        if conversation.user_id != user_id:
            raise ForbiddenError("Access denied")
        await self.db.delete(conversation)
        await self.db.commit()
        return conversation
