import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Message
from src.repositories.message_repository import MessageRepository
from src.schemas.message_schema import MessageCreate


class MessageService:
    def __init__(self, db: AsyncSession):
        self.repo = MessageRepository(db)

    async def create_message(self, payload: MessageCreate) -> Message:
        message = Message(
            conversation_id=payload.conversation_id,
            role=payload.role,
            content=payload.content,
        )
        return await self.repo.create_message(message)

    async def get_all_conversation_messages(self, convo_id: uuid.UUID) -> list[Message]:
        return await self.repo.get_all_conversation_messages(convo_id)
