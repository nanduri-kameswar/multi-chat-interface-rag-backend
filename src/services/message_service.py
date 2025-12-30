import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Message
from src.repositories.message_repository import MessageRepository
from src.schemas.message_schema import MessageCreate, MessageResponse


class MessageService:
    def __init__(self, db: AsyncSession):
        self.repo = MessageRepository(db)

    async def create_message(self, payload: MessageCreate) -> MessageResponse:
        message = Message(
            conversation_id=payload.conversation_id,
            role=payload.role,
            content=payload.content,
        )
        db_message = await self.repo.create_message(message)
        return MessageResponse(
            role=db_message.role,
            content=db_message.content,
            created_at=db_message.created_at,
        )

    async def get_recent_k_conversation_messages(
        self, convo_id: uuid.UUID, k: int = 5
    ) -> list[MessageResponse]:
        db_messages: list[Message] = await self.repo.get_recent_k_conversation_messages(
            convo_id, k
        )
        messages: list[MessageResponse] = [
            MessageResponse(
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at,
            )
            for msg in db_messages
        ]
        return messages
