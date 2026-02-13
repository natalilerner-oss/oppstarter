from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ai_enabled: bool = Field(default=False, alias="AI_ENABLED")
    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-1.5-flash", alias="GEMINI_MODEL")
    ai_timeout_seconds: int = Field(default=20, alias="AI_TIMEOUT_SECONDS")
    ai_max_retries: int = Field(default=5, alias="AI_MAX_RETRIES")
    ai_base_url: str = Field(
        default="https://generativelanguage.googleapis.com/v1beta",
        alias="AI_BASE_URL",
    )


settings = Settings()
