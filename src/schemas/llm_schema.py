import uuid
from typing import Literal

from pydantic import BaseModel, Field

from src.schemas.base_schema import ORMBase


class LLMRequest(BaseModel):
    query: str = Field(...)
    conversation_id: uuid.UUID


class LLMResponse(ORMBase):
    query: str
    answer: str
    reference: dict[int, dict[str, str | int]]
    status: Literal[200, 202, 500] = 202
