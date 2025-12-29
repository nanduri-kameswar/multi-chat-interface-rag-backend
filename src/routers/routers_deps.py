from typing import Annotated, TypeAlias

from fastapi import Depends

from src.db.db_deps import AsyncDb_Dependency, PGVectorStore_Dependency
from src.services.conversation_service import ConversationService
from src.services.document_service import DocumentService
from src.services.message_service import MessageService
from src.services.user_service import UserService


# user service dependency
def get_user_service(db: AsyncDb_Dependency) -> UserService:
    return UserService(db)


UserService_Dependency: TypeAlias = Annotated[
    UserService,
    Depends(get_user_service),
]


# conversation service dependency
def get_conversation_service(db: AsyncDb_Dependency) -> ConversationService:
    return ConversationService(db)


ConversationService_Dependency: TypeAlias = Annotated[
    ConversationService, Depends(get_conversation_service)
]


# message service dependency
def get_message_service(db: AsyncDb_Dependency) -> MessageService:
    return MessageService(db)


MessageService_Dependency: TypeAlias = Annotated[
    MessageService,
    Depends(get_message_service),
]


# document service dependency
def get_document_service(
    db: AsyncDb_Dependency, vector_store: PGVectorStore_Dependency
) -> DocumentService:
    return DocumentService(db, vector_store)


DocumentService_Dependency: TypeAlias = Annotated[
    DocumentService, Depends(get_document_service)
]
