from typing import Annotated, TypeAlias

from fastapi import Depends

from src.db.db_deps import AsyncDb_Dependency
from src.services.conversation_service import ConversationService
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
