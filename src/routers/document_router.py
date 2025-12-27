from uuid import UUID

from fastapi import APIRouter

from src.auth.auth_deps import CurrentUser_Dependency
from src.models.enums import DocumentStatus
from src.schemas.document_schema import DocumentCreate, DocumentResponse

from .routers_deps import DocumentService_Dependency

router = APIRouter(
    prefix="/document",
    tags=["document"],
)


@router.post("/create", response_model=DocumentResponse)
async def create_document(
    payload: DocumentCreate,
    jwt: CurrentUser_Dependency,
    service: DocumentService_Dependency,
):
    return await service.create_document(
        payload.file_name, payload.conversation_id, UUID(jwt.get("user_id"))
    )


@router.get("/read/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: UUID, jwt: CurrentUser_Dependency, service: DocumentService_Dependency
):
    return await service.get_document(UUID(jwt.get("user_id")), document_id)


@router.get("/user/read-all", response_model=list[DocumentResponse])
async def get_all_user_documents(
    jwt: CurrentUser_Dependency, service: DocumentService_Dependency
):
    return await service.get_all_user_documents(UUID(jwt.get("user_id")))


@router.get("/conversation/{conversation_id}", response_model=list[DocumentResponse])
async def get_all_conversation_documents(
    conversation_id: UUID,
    jwt: CurrentUser_Dependency,
    service: DocumentService_Dependency,
):
    return await service.get_all_conversation_documents(
        UUID(jwt.get("user_id")), conversation_id
    )


@router.put("/update-status/{document_id}")
async def modify_document_status(
    document_id: UUID,
    status: DocumentStatus,
    jwt: CurrentUser_Dependency,
    service: DocumentService_Dependency,
):
    return await service.modify_document_status(
        UUID(jwt.get("user_id")), document_id, status
    )


@router.delete("/delete/{document_id}")
async def delete_document(
    document_id: UUID, jwt: CurrentUser_Dependency, service: DocumentService_Dependency
):
    return await service.delete_document(UUID(jwt.get("user_id")), document_id)
