from enum import Enum


class LangChainProviderType(str, Enum):
    OLLAMA_LOCAL = "ollama-local"
    GEMINI = "gemini"


class LangChainTextSplitterType(str, Enum):
    RECURSIVE = "recursive"
