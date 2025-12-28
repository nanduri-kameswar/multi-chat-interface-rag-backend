from src.core.config import settings

from .gemini_embedding import GeminiEmbeddingProvider


def get_embedding_provider():
    provider = settings.EMBEDDING_PROVIDER
    match provider:
        case "local":
            return GeminiEmbeddingProvider
        case _:
            return GeminiEmbeddingProvider
