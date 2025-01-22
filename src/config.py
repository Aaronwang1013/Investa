import os 

from pydantic_settings import BaseSettings, SettingsConfigDict


class _settings(BaseSettings):
    USERNAME: str = ""
    PASSWORD: str = ""
    EMAIL: str = ""
    APP_DEBUG: bool = False
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

    #mysql
    DB_HOST: str = ""
    DB_PORT: int = 5432
    MYSQL_DB_NAME: str = ""
    MYSQL_DB_USER: str = ""
    MYSQL_DB_PASSWORD: str = ""



settings = _settings()