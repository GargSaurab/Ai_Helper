from urllib.parse import quote_plus

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

import logging


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    LOGGER_LEVEL: str = logging.INFO

    APP_NAME: str = "Coding Ai Helper"
    APP_VERSION: str = "0.0.1"
    ENVIRONMENT: str = "dev"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
    ## JWT Secret Key for signing and verifying JWT tokens
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
        

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.DB_USER}:"
            f"{quote_plus(self.DB_PASSWORD)}"
            f"@{self.DB_HOST}:{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )


settings = Settings()
