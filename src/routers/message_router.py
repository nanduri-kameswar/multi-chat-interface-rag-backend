import uuid

from fastapi import APIRouter

from src.auth.auth_deps import CurrentUser_Dependency
from src.models import Message
from src.schemas.message_schema import MessageCreate, MessageResponse

from .routers_deps import MessageService_Dependency

router = APIRouter(prefix="/message", tags=["message"])


@router.post("/create", response_model=MessageResponse)
async def create_message(
    payload: MessageCreate,
    jwt: CurrentUser_Dependency,
    service: MessageService_Dependency,
) -> Message:
    return await service.create_message(payload)


@router.get("/read/{k}", response_model=list[MessageResponse])
async def get_recent_k_conversation_messages(
    convo_id: uuid.UUID,
    k: int,
    jwt: CurrentUser_Dependency,
    service: MessageService_Dependency,
) -> list[Message]:
    return await service.get_recent_k_conversation_messages(convo_id, k)
