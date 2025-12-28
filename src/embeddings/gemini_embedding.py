from google import genai
from google.genai import types

from ..core.config import settings
from .base_embedding import BaseEmbedding


class GeminiEmbeddingProvider(BaseEmbedding):
    def __init__(self):
        self.model = "gemini-embedding-001"

    def embed(self, texts: list[str]) -> list[list[float]]:
        with genai.Client(api_key=settings.GEMINI_API_KEY) as client:
            response = client.models.embed_content(
                model=self.model,
                contents=texts,
                config=types.EmbedContentConfig(
                    output_dimensionality=settings.VECTOR_SIZE
                ),
            )
            return [item.values for item in response.embeddings]
