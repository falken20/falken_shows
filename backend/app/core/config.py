from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application-wide configuration loaded from environment variables and .env files.

    All settings can be overridden via environment variables (case-sensitive).
    Production deployments must supply strong secrets via Google Secret Manager
    (see infrastructure/terraform/main.tf for secret_key_ref bindings).

    Security invariants enforced at startup:
        - CORS_ORIGINS may not be empty or contain ``'*'``.
        - In production, JWT_SECRET_KEY must be ≥32 chars and not start with ``change-me``.
        - In production, ADMIN_PASSWORD must be ≥12 chars and not start with ``change-me``.
        - ACCESS_TOKEN_EXPIRE_MINUTES must be in the range [1, 1440].
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ── Application ────────────────────────────────────────────
    APP_NAME: str = "Live Memories"
    APP_ENV: Literal["development", "testing", "production"] = "development"
    APP_DEBUG: bool = False
    APP_VERSION: str = "0.1.0"

    # ── Server ─────────────────────────────────────────────────
    BACKEND_HOST: str = "0.0.0.0"  # noqa: S104 – intentional dev default, overridden via env var
    BACKEND_PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:5173"

    # ── Database ───────────────────────────────────────────────
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/live_memories.db"

    # ── JWT ────────────────────────────────────────────────────
    JWT_SECRET_KEY: str = "change-me-to-a-long-random-string-in-production"  # noqa: S105 – placeholder, must be overridden in production via env var
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ── Admin user ─────────────────────────────────────────────
    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str = "change-me-in-production"  # noqa: S105 – placeholder, must be overridden in production via env var

    # ── Storage ────────────────────────────────────────────────
    STORAGE_BACKEND: Literal["local", "gcs"] = "local"
    LOCAL_STORAGE_PATH: str = "./data/uploads"
    GCS_BUCKET_NAME: str = ""
    GCP_PROJECT_ID: str = ""

    # ── File uploads ───────────────────────────────────────────
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_IMAGE_TYPES: str = "image/jpeg,image/png,image/webp"

    # ── CORS ───────────────────────────────────────────────────
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:4173"]

    # ── Localisation ───────────────────────────────────────────
    DEFAULT_LANGUAGE: str = "es"
    DEFAULT_CURRENCY: str = "EUR"
    DEFAULT_TIMEZONE: str = "Europe/Madrid"

    # ── Logging ────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        """Accept CORS_ORIGINS as a comma-separated string or a JSON list."""
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return [origin.strip() for origin in value if origin.strip()]

    @field_validator("ACCESS_TOKEN_EXPIRE_MINUTES")
    @classmethod
    def validate_access_token_expiry(cls, value: int) -> int:
        """Enforce a sensible token lifetime: between 1 minute and 24 hours."""
        if value <= 0:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be greater than 0")
        if value > 24 * 60:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be 1440 or lower")
        return value

    @model_validator(mode="after")
    def validate_security_settings(self) -> "Settings":
        """Cross-field security validation executed after all fields are populated."""
        if not self.CORS_ORIGINS:
            raise ValueError("CORS_ORIGINS must include at least one origin")
        if "*" in self.CORS_ORIGINS:
            raise ValueError("CORS_ORIGINS cannot contain '*'")

        if self.APP_ENV == "production":
            if self.JWT_SECRET_KEY.startswith("change-me") or len(self.JWT_SECRET_KEY) < 32:
                raise ValueError(
                    "JWT_SECRET_KEY must be overridden in production and have at least 32 characters"
                )
            if self.ADMIN_PASSWORD.startswith("change-me") or len(self.ADMIN_PASSWORD) < 12:
                raise ValueError(
                    "ADMIN_PASSWORD must be overridden in production and have at least 12 characters"
                )

        return self

    @property
    def allowed_image_types_list(self) -> list[str]:
        """ALLOWED_IMAGE_TYPES parsed into a list of MIME-type strings."""
        return [t.strip() for t in self.ALLOWED_IMAGE_TYPES.split(",") if t.strip()]

    @property
    def max_upload_size_bytes(self) -> int:
        """MAX_UPLOAD_SIZE_MB converted to bytes."""
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    """Return the singleton Settings instance (result is cached by lru_cache)."""
    return Settings()


settings = get_settings()
