import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.exceptions import NotFoundError
from src.models import Conversation, Message


class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(self, message: Message) -> Message:
        result = await self.db.execute(
            select(Conversation).filter(Conversation.id == message.conversation_id)
        )
        convo: Conversation | None = result.scalar_one_or_none()
        if not convo:
            raise NotFoundError("Conversation not found")
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_all_conversation_messages(self, convo_id: uuid.UUID) -> list[Message]:
        result = await self.db.execute(
            select(Message)
            .filter(Message.conversation_id == convo_id)
            .order_by(Message.created_at)
        )
        messages: list[Message] = list(result.scalars())
        return messages
