from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, UploadFile, status

from src.auth.auth_deps import CurrentUser_Dependency
from src.schemas.document_schema import DocumentResponse

from ..schemas.document_chunk_schema import DocumentChunkResponse
from .routers_deps import DocumentService_Dependency

router = APIRouter(
    prefix="/document",
    tags=["document"],
)


@router.post(
    "/upload", response_model=DocumentResponse, status_code=status.HTTP_202_ACCEPTED
)
async def upload_pdf(
    file: UploadFile,
    convo_id: UUID,
    jwt: CurrentUser_Dependency,
    service: DocumentService_Dependency,
    background_tasks: BackgroundTasks,
):
    return await service.create_document(
        file,
        convo_id,
        UUID(jwt.get("user_id")),
        background_tasks,
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


@router.delete("/delete/{document_id}")
async def delete_document(
    document_id: UUID, jwt: CurrentUser_Dependency, service: DocumentService_Dependency
):
    return await service.delete_document(UUID(jwt.get("user_id")), document_id)


@router.get(
    "/chunks/read-all/{document_id}", response_model=list[DocumentChunkResponse]
)
async def get_all_document_chunks(
    document_id: UUID, jwt: CurrentUser_Dependency, service: DocumentService_Dependency
):
    return await service.get_all_document_chunks(UUID(jwt.get("user_id")), document_id)


@router.get("/conversation/similar/{text}", response_model=list[DocumentChunkResponse])
async def get_similar_document_chunks(
    text: str,
    convo_id: UUID,
    jwt: CurrentUser_Dependency,
    service: DocumentService_Dependency,
):
    user_id: UUID = UUID(jwt.get("user_id"))
    document_ids = await service.get_all_conversation_documents(
        user_id, convo_id, only_doc_ids=True
    )
    return await service.get_similar_document_chunks(text, document_ids)
