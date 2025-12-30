import uuid

from fastapi import APIRouter

from src.auth.auth_deps import CurrentUser_Dependency
from src.routers.routers_deps import DocumentService_Dependency, LLMService_Dependency
from src.schemas.llm_schema import LLMRequest, LLMResponse

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
) -> LLMResponse:
    user_id: uuid.UUID = uuid.UUID(jwt.get("user_id"))
    document_ids = await document_service.get_all_conversation_documents(
        user_id, payload.conversation_id, only_doc_ids=True
    )
    result = await llm_service.run_llm(payload.query, [], document_ids)
    return result
