from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings

from src.core.config import settings
from src.core.env_enums import LangChainProviderType


def get_embedding():
    embedding_type = settings.LANGCHAIN_PROVIDER
    match embedding_type:
        case LangChainProviderType.OLLAMA_LOCAL:
            return OllamaEmbeddings(
                base_url=settings.OLLAMA_LOCALHOST,
                model="mxbai-embed-large",
                validate_model_on_init=True,
            )
        case LangChainProviderType.GEMINI:
            return GoogleGenerativeAIEmbeddings(
                model="gemini-embedding-001",
                api_key=settings.PROVIDER_API_KEY,
                output_dimensionality=settings.VECTOR_SIZE,
            )
        case _:
            raise ValueError(f"Unsupported splitter type: {embedding_type}")
