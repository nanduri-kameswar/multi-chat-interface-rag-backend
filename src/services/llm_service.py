import uuid
from typing import Any

from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.history_aware_retriever import (
    create_history_aware_retriever,
)
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.callbacks import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
)
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_postgres import PGVectorStore

from src.repositories.document_chunk_repository import (
    DocumentChunkVectorStoreRepository,
)
from src.schemas.llm_schema import LLMResponse
from src.utilities.llm_model_utility import get_llm_chat
from src.utilities.prompt_utility import REPHRASE_PROMPT, RETRIEVAL_QA_CHAT_PROMPT


class LLMService:
    def __init__(self, vector_store: PGVectorStore):
        self.llm = get_llm_chat()
        self.vector_store = vector_store

    async def run_llm(
        self, query: str, chat_history: list[dict[str, Any]], doc_ids: list[uuid.UUID]
    ) -> LLMResponse:
        retrieval_qa_chat_prompt = RETRIEVAL_QA_CHAT_PROMPT

        stuff_documents_chain = create_stuff_documents_chain(
            llm=self.llm, prompt=retrieval_qa_chat_prompt
        )

        chunk_retriever = ChunkRetriever(
            chunk_vector_store=DocumentChunkVectorStoreRepository(self.vector_store),
            document_ids=doc_ids,
        )

        rephrase_prompt = REPHRASE_PROMPT
        history_aware_retriever = create_history_aware_retriever(
            llm=self.llm, retriever=chunk_retriever, prompt=rephrase_prompt
        )

        qa = create_retrieval_chain(
            retriever=history_aware_retriever, combine_docs_chain=stuff_documents_chain
        )

        result = await qa.ainvoke({"input": query, "chat_history": chat_history})
        llm_response = LLMService.to_llm_response(result)
        return llm_response

    @staticmethod
    def to_llm_response(data: dict) -> LLMResponse:
        references: dict[int, dict[str, str]] = {}

        for idx, doc in enumerate(data.get("context", []), start=1):
            metadata = doc.metadata or {}
            references[idx] = {
                "source": metadata.get("source"),
                "page": metadata.get("page"),
                "content": doc.page_content,
            }

        return LLMResponse(
            query=data.get("input"), answer=data.get("answer"), reference=references
        )


class ChunkRetriever(BaseRetriever):
    chunk_vector_store: DocumentChunkVectorStoreRepository
    document_ids: list[uuid.UUID]

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> list[Document]:
        return self.chunk_vector_store.similarity_search_sync(query, self.document_ids)

    async def _aget_relevant_documents(
        self,
        query: str,
        *,
        run_manager: AsyncCallbackManagerForRetrieverRun,
        **kwargs: Any,
    ) -> list[Document]:
        return await self.chunk_vector_store.similarity_search(query, self.document_ids)
