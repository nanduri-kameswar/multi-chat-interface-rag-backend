import uuid
from collections import defaultdict

from langchain_core.documents import Document


def add_chunk_metadata(
    docs: list[Document], user_id: uuid.UUID, convo_id: uuid.UUID, doc_id: uuid.UUID
) -> list[Document]:
    page_counters = defaultdict(int)
    for doc in docs:
        page = doc.metadata.get("page", 0)

        chunk_index = page_counters[page]
        page_counters[page] += 1

        doc.metadata["chunk_index"] = chunk_index
        doc.metadata["document_id"] = str(doc_id)
        doc.metadata["user_id"] = str(user_id)
        doc.metadata["conversation_id"] = str(convo_id)
    return docs
