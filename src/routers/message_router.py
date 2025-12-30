import uuid

from fastapi import APIRouter

from src.auth.auth_deps import CurrentUser_Dependency
from src.models import Message
from src.schemas.message_schema import MessageCreate, MessageResponse

from .routers_deps import MessageService_Dependency

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/create", response_model=MessageResponse)
async def create_message(
    payload: MessageCreate,
    jwt: CurrentUser_Dependency,
    service: MessageService_Dependency,
) -> MessageResponse:
    return await service.create_message(payload)


@router.get("/", response_model=list[MessageResponse])
async def get_recent_k_conversation_messages(
    conversation_id: uuid.UUID,
    limit: int | None,
    jwt: CurrentUser_Dependency,
    service: MessageService_Dependency,
) -> list[MessageResponse]:
    return await service.get_recent_k_conversation_messages(conversation_id, limit)
