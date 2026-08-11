import sys
from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: Literal["local", "dev", "test", "prod"] = "local"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    api_key: SecretStr = Field(default=SecretStr("default_api_key"))
    app_name: str = "My API"

    @property
    def is_pytest(self) -> bool:
        return "pytest" in sys.modules


@lru_cache
def get_settings() -> Settings:
    return Settings()
