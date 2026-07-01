from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from ai_resume_analyzer.constants.logging import VALID_LOG_LEVELS
from ai_resume_analyzer.constants.uploads import (
    DEFAULT_ALLOWED_FILE_TYPES,
    DEFAULT_MAX_UPLOAD_SIZE_MB,
    DEFAULT_UPLOAD_DIRECTORY,
)

AppEnvironment = Literal["development", "test", "staging", "production"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "ai-resume-analyzer"
    app_env: AppEnvironment = "development"
    debug: bool = False
    log_level: str = "INFO"

    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_resume_analyzer"
    )
    database_echo: bool = False
    database_pool_size: int = Field(default=5, ge=1)
    database_max_overflow: int = Field(default=10, ge=0)
    database_pool_timeout: int = Field(default=30, ge=1)
    database_pool_recycle: int = Field(default=1800, ge=1)

    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = Field(default=30, ge=1)

    upload_directory: str = DEFAULT_UPLOAD_DIRECTORY
    max_upload_size_mb: int = Field(default=DEFAULT_MAX_UPLOAD_SIZE_MB, ge=1)
    allowed_file_types: list[str] = Field(
        default_factory=lambda: list(DEFAULT_ALLOWED_FILE_TYPES)
    )

    request_id_header: str = "X-Request-ID"

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-1.5-flash"

    cors_allow_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:8000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5174",
        ]
    )
    cors_allow_origin_regex: str | None = r"https://.*\.vercel\.app"
    cors_allow_credentials: bool = False
    cors_allow_methods: list[str] = Field(
        default_factory=lambda: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )
    cors_allow_headers: list[str] = Field(default_factory=lambda: ["*"])

    @field_validator("debug", mode="before")
    @classmethod
    def normalize_debug(cls, value: object) -> object:
        if not isinstance(value, str):
            return value

        normalized = value.strip().lower()
        if normalized == "debug":
            return True
        if normalized == "release":
            return False
        return value

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in VALID_LOG_LEVELS:
            valid_levels = ", ".join(sorted(VALID_LOG_LEVELS))
            msg = f"LOG_LEVEL must be one of: {valid_levels}"
            raise ValueError(msg)
        return normalized

    @field_validator("jwt_secret_key")
    @classmethod
    def validate_jwt_secret_key(cls, value: str) -> str:
        if not value.strip():
            msg = "JWT_SECRET_KEY must not be empty"
            raise ValueError(msg)
        return value

    @field_validator("upload_directory")
    @classmethod
    def normalize_upload_directory(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            msg = "UPLOAD_DIRECTORY must not be empty"
            raise ValueError(msg)
        return normalized.rstrip("/\\")

    @field_validator("allowed_file_types")
    @classmethod
    def normalize_allowed_file_types(cls, value: list[str]) -> list[str]:
        normalized = [content_type.strip().lower() for content_type in value]
        allowed_file_types = [
            content_type for content_type in normalized if content_type
        ]
        if not allowed_file_types:
            msg = "ALLOWED_FILE_TYPES must contain at least one content type"
            raise ValueError(msg)
        return allowed_file_types

    @field_validator("gemini_api_key")
    @classmethod
    def normalize_gemini_api_key(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("gemini_model")
    @classmethod
    def normalize_gemini_model(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            msg = "GEMINI_MODEL must not be empty"
            raise ValueError(msg)
        return normalized

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        if self.app_env != "production":
            return self

        if self.debug:
            msg = "DEBUG must be false in production"
            raise ValueError(msg)
        if self.jwt_secret_key == "change-me-in-production":
            msg = "JWT_SECRET_KEY must be changed in production"
            raise ValueError(msg)
        if self.gemini_api_key is None:
            msg = "GEMINI_API_KEY must be configured in production"
            raise ValueError(msg)

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
