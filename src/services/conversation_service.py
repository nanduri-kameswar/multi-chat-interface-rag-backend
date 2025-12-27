import uuid
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Conversation
from src.repositories.conversation_repository import ConversationRepository
from src.schemas.conversation_schema import ConversationUpdate


class ConversationService:
    def __init__(self, db: AsyncSession):
        self.repo = ConversationRepository(db)

    async def create_conversation(self, title: str, user_id: uuid.UUID) -> Conversation:
        conversation = Conversation(title=title, user_id=user_id)
        return await self.repo.create_conversation(conversation)

    async def get_conversation(
        self, conversation_id: uuid.UUID, user_id: uuid.UUID
    ) -> Conversation:
        return await self.repo.get_conversation(conversation_id, user_id)

    async def get_all_conversations(self, user_id: uuid.UUID) -> List[Conversation]:
        return await self.repo.get_all_conversations(user_id)

    async def update_conversation(
        self,
        updated_conversation: ConversationUpdate,
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Conversation:
        return await self.repo.update_conversation(
            updated_conversation, conversation_id, user_id
        )

    async def delete_conversation(
        self, conversation_id: uuid.UUID, user_id: uuid.UUID
    ) -> Conversation:
        return await self.repo.delete_conversation(conversation_id, user_id)
