from contextlib import asynccontextmanager
from typing import AsyncGenerator

from langchain_postgres import PGEngine, PGVectorStore
from langchain_postgres.v2.indexes import HNSWIndex
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings
from src.utilities.embedding_utility import get_embedding

engine = create_async_engine(settings.DATABASE_URL)
pg_engine = PGEngine.from_engine(engine=engine)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, autocommit=False, autoflush=False
)

class Base(DeclarativeBase):
    pass

"""
Initialize pg vector store
"""
@asynccontextmanager
async def init_vector_store() -> AsyncGenerator[PGVectorStore, None]:
    index = HNSWIndex("hnsw-index")
    vector_store = await PGVectorStore.create(
        engine=pg_engine,
        table_name="document_chunks",
        embedding_service=get_embedding(),
        id_column="id",
        embedding_column="embedding",
        content_column="content",
        metadata_columns=["document_id"],
        metadata_json_column="cmetadata",
    )
    try:
        await vector_store.aapply_vector_index(index)
        yield vector_store
    finally:
        await vector_store.adrop_vector_index("hnsw-index")
