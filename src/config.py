import os 

from pydantic_settings import BaseSettings, SettingsConfigDict


class _settings(BaseSettings):
    USERNAME: str = ""
    PASSWORD: str = ""
    EMAIL: str = ""
    
    #auth
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0

    #Oauth2.0
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_AUTH_URL: str = ""
    GOOGLE_TOKEN_URL: str = ""

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )



settings = _settings()