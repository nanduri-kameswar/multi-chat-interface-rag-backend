from typing import Annotated, AsyncGenerator, TypeAlias

from fastapi import Depends, Request
from langchain_postgres import PGVectorStore
from sqlalchemy.ext.asyncio import AsyncSession

from .connection import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


AsyncDb_Dependency: TypeAlias = Annotated[AsyncSession, Depends(get_db)]


async def get_vector_store(request: Request) -> PGVectorStore:
    return request.app.state.vector_store


PGVectorStore_Dependency: TypeAlias = Annotated[
    PGVectorStore, Depends(get_vector_store)
]
