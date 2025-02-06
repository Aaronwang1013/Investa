from pydantic_settings import BaseSettings, SettingsConfigDict


class _settings(BaseSettings):
    USERNAME: str = ""
    PASSWORD: str = ""
    EMAIL: str = ""
    APP_DEBUG: bool = False
    # JWT
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Oauth2.0
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    FACEBOOK_CLIENT_ID: str = ""
    FACEBOOK_CLIENT_SECRET: str = ""
    APPLE_CLIENT_ID: str = ""
    APPLE_CLIENT_SECRET: str = ""

    OAUTH_PROVIDERS: list = ["google", "facebook", "apple"]

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # mysql
    DB_HOST: str = ""
    DB_PORT: int = 5432
    MYSQL_DB_NAME: str = ""
    MYSQL_DB_USER: str = ""
    MYSQL_DB_PASSWORD: str = ""


settings = _settings()
