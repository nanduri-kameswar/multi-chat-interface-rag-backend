from enum import Enum


class LangChainEmbeddingType(str, Enum):
    OLLAMA_LOCAL = "ollama-local"
    GEMINI = "gemini"


class LangChainTextSplitterType(str, Enum):
    RECURSIVE = "recursive"
