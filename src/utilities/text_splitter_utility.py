from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.core.config import settings
from src.core.env_enums import LangChainTextSplitterType


def get_text_splitter():
    text_splitter_type = settings.TEXT_SPLITTER
    match text_splitter_type:
        case LangChainTextSplitterType.RECURSIVE:
            return RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP
            )
        case _:
            raise ValueError(f"Unsupported splitter type: {LangChainTextSplitterType}")
