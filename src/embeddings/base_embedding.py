from abc import ABC, abstractmethod

from src.core.config import AppSettings


class BaseEmbedding(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """
        Takes a list of texts and returns a list of embeddings.
        """
        pass
