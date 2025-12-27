from typing import Annotated, TypeAlias

from fastapi import Depends

from src.db.db_deps import AsyncDb_Dependency
from src.services.user_service import UserService


# user service dependency
def get_user_service(db: AsyncDb_Dependency) -> UserService:
    return UserService(db)


UserService_Dependency: TypeAlias = Annotated[
    UserService,
    Depends(get_user_service),
]
