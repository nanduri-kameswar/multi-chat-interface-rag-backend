from uuid import UUID

from fastapi import APIRouter

from src.auth.auth_deps import CurrentUser_Dependency
from src.schemas.conversation_schema import (ConversationCreate,
                                             ConversationResponse,
                                             ConversationUpdate)

from .routers_deps import ConversationService_Dependency

router = APIRouter(prefix="/conversation", tags=["conversation"])


@router.post("/create", response_model=ConversationResponse)
async def create_conversation(
    payload: ConversationCreate,
    jwt: CurrentUser_Dependency,
    service: ConversationService_Dependency,
):
    return await service.create_conversation(payload.title, UUID(jwt.get("user_id")))


@router.get("/read/{convo_id}", response_model=ConversationResponse)
async def get_conversation(
    convo_id: UUID,
    jwt: CurrentUser_Dependency,
    service: ConversationService_Dependency,
):
    return await service.get_conversation(convo_id, UUID(jwt.get("user_id")))


@router.get("/read-all", response_model=list[ConversationResponse])
async def get_all_conversations(
    jwt: CurrentUser_Dependency, service: ConversationService_Dependency
):
    return await service.get_all_conversations(UUID(jwt.get("user_id")))


@router.patch("/update/{convo_id}", response_model=ConversationResponse)
async def update_conversation(
    updated_conversation: ConversationUpdate,
    convo_id: UUID,
    jwt: CurrentUser_Dependency,
    service: ConversationService_Dependency,
):
    return await service.update_conversation(
        updated_conversation, convo_id, UUID(jwt.get("user_id"))
    )


@router.delete("/delete/{convo_id}", response_model=ConversationResponse)
async def delete_conversation(
    convo_id: UUID,
    jwt: CurrentUser_Dependency,
    service: ConversationService_Dependency,
):
    return await service.delete_conversation(convo_id, UUID(jwt.get("user_id")))


router = APIRouter(prefix="/conversation", tags=["conversation"])


@router.post("/create", response_model=ConversationResponse)
async def create_conversation(
    payload: ConversationCreate,
    jwt: CurrentUser_Dependency,
    service: ConversationService_Dependency,
):
    return await service.create_conversation(payload.title, UUID(jwt.get("user_id")))


@router.get("/read/{convo_id}", response_model=ConversationResponse)
async def get_conversation(
    convo_id: UUID,
    jwt: CurrentUser_Dependency,
    service: ConversationService_Dependency,
):
    return await service.get_conversation(convo_id, UUID(jwt.get("user_id")))


@router.get("/read-all", response_model=list[ConversationResponse])
async def get_all_conversations(
    jwt: CurrentUser_Dependency, service: ConversationService_Dependency
):
    return await service.get_all_conversations(UUID(jwt.get("user_id")))


@router.patch("/update/{convo_id}", response_model=ConversationResponse)
async def update_conversation(
    updated_conversation: ConversationUpdate,
    convo_id: UUID,
    jwt: CurrentUser_Dependency,
    service: ConversationService_Dependency,
):
    return await service.update_conversation(
        updated_conversation, convo_id, UUID(jwt.get("user_id"))
    )


@router.delete("/delete/{convo_id}", response_model=ConversationResponse)
async def delete_conversation(
    convo_id: UUID,
    jwt: CurrentUser_Dependency,
    service: ConversationService_Dependency,
):
    return await service.delete_conversation(convo_id, UUID(jwt.get("user_id")))
