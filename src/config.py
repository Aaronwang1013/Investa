import os 

from pydantic_settings import BaseSettings, SettingsConfigDict


class _settings(BaseSettings):
    USERNAME: str = ""
    PASSWORD: str = ""
    EMAIL: str = ""

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )



settings = _settings()