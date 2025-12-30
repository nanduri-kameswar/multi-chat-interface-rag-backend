from datetime import timedelta
from typing import List, Union

from pydantic import Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.env_enums import LangChainProviderType, LangChainTextSplitterType

# ----------------------------
# APP SETTINGS
# ----------------------------


class AppSettings(BaseSettings):
    # App
    APP_NAME: str = "FastAPI App"
    API_PREFIX: str = "/api"
    DEBUG: bool = False

    # Security
    JWT_SECRET_KEY: str | None = None
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_IN: timedelta = Field(default=timedelta(minutes=15))
    REFRESH_JWT_EXPIRES_IN: timedelta = Field(default=timedelta(days=1))

    # Database
    DATABASE_TEMPLATE_URL: str | None = None
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""
    DB_HOST: str = ""
    DB_PORT: str = ""

    # Vector DB Configs
    VECTOR_SIZE: int = 1536
    LANGCHAIN_PROVIDER: LangChainProviderType = LangChainProviderType.GEMINI
    TEXT_SPLITTER: LangChainTextSplitterType = LangChainTextSplitterType.RECURSIVE
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    SIMILARITY_SEARCH_K: int = 20
    OLLAMA_LOCALHOST: str | None = None

    # API Keys
    PROVIDER_API_KEY: str = ""

    # CORS
    ALLOWED_ORIGINS: Union[str, List[str]] = Field(default=["*"])

    # --------------------------
    # Computed field
    # --------------------------
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return self.DATABASE_TEMPLATE_URL.format(
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            name=self.DB_NAME,
            host=self.DB_HOST,
            port=self.DB_PORT,
        )

    # ----------------------------
    # Validators
    # ----------------------------

    @field_validator("JWT_EXPIRES_IN", mode="before")
    @classmethod
    def parse_jwt_expires_in(cls, v):
        if isinstance(v, timedelta):
            return v
        if isinstance(v, (int, str)):
            return timedelta(minutes=int(v))
        raise ValueError("Invalid JWT_EXPIRES_IN")

    @field_validator("REFRESH_JWT_EXPIRES_IN", mode="before")
    @classmethod
    def parse_refresh_jwt_expires_in(cls, v):
        if isinstance(v, timedelta):
            return v
        if isinstance(v, (int, str)):
            return timedelta(days=int(v))
        raise ValueError("Invalid REFRESH_JWT_EXPIRES_IN")

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value):
        if not value:
            return []
        if isinstance(value, str):
            return [v.strip() for v in value.split(",") if v.strip()]
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Singleton
settings = AppSettings()
