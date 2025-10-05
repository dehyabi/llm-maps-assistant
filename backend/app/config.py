from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    app_name: str = "LLM Maps Assistant API"
    environment: str = Field(default="development", validation_alias="ENVIRONMENT")
    allowed_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173", "http://localhost:3000"])  # update as needed

    google_maps_api_key: str = Field(min_length=10, validation_alias="GOOGLE_MAPS_API_KEY")

    ratelimit_requests: int = Field(default=60, ge=1)
    ratelimit_window_seconds: int = Field(default=60, ge=1)

@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[arg-type]
