import uuid
from typing import Any

from fastapi import APIRouter

from src.auth.auth_deps import CurrentUser_Dependency
from src.models.enums import MessageRole
from src.routers.routers_deps import (
    DocumentService_Dependency,
    LLMService_Dependency,
    MessageService_Dependency,
)
from src.schemas.llm_schema import LLMRequest, LLMResponse
from src.schemas.message_schema import MessageCreate, MessageResponse
from src.utilities.chat_message_utility import convert_messages_to_chat_history

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("/query", response_model=LLMResponse)
async def query(
    payload: LLMRequest,
    jwt: CurrentUser_Dependency,
    llm_service: LLMService_Dependency,
    document_service: DocumentService_Dependency,
    message_service: MessageService_Dependency,
) -> LLMResponse:
    user_id: uuid.UUID = uuid.UUID(jwt.get("user_id"))
    document_ids = await document_service.get_all_conversation_documents(
        user_id, payload.conversation_id, only_doc_ids=True
    )
    # retrieve k recent message for chat history
    recent_k_messages: list[MessageResponse] | None = (
        await message_service.get_recent_k_conversation_messages(
            payload.conversation_id
        )
    )
    chat_history: list[dict[str, Any]] = (
        convert_messages_to_chat_history(recent_k_messages) if recent_k_messages else []
    )
    # add human message to db
    human_message = MessageCreate.model_validate(
        {payload.conversation_id, MessageRole.USER, payload.query}
    )
    _ = await message_service.create_message(human_message)
    # await the llm response result
    result = await llm_service.run_llm(payload.query, chat_history, document_ids)
    # add assistant message to db
    assistant_message = MessageCreate.model_validate(
        {payload.conversation_id, MessageRole.ASSISTANT, result.answer}
    )
    _ = await message_service.create_message(assistant_message)
    # return the result
    return result
