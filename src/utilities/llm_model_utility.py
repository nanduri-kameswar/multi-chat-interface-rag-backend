from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

from src.core.config import settings
from src.core.env_enums import LangChainProviderType


def get_llm_chat():
    provider = settings.LANGCHAIN_PROVIDER
    match provider:
        case LangChainProviderType.OLLAMA_LOCAL:
            return ChatOllama(
                model="gemma3:4b",
                base_url=settings.OLLAMA_LOCALHOST,
            )
        case LangChainProviderType.GEMINI:
            return ChatGoogleGenerativeAI(
                model="gemini-embedding-001", api_key=settings.PROVIDER_API_KEY
            )
        case _:
            raise ValueError(f"Unsupported chat model type: {provider}")
