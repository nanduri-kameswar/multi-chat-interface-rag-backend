from typing import Any
from src.schemas.message_schema import MessageResponse


def convert_messages_to_chat_history(messages: list[MessageResponse]) -> list[dict[str, Any]]:
    return [
        {message.role: message.content} for message in messages
    ]
