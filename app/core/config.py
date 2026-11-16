from urllib.parse import quote_plus

from pydantic import computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    LOGGER_LEVEL: str = "INFO"
    SQL_ECHO: bool = False

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

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, value: str) -> str:
        if len(value.encode("utf-8")) < 32:
            raise ValueError("SECRET_KEY must be at least 32 bytes long")
        return value

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (
        15  # Default expiration time in minutes for access tokens
    )
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080

    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    AUTH_RATE_LIMIT_WINDOW_SECONDS: int = 60
    LOGIN_RATE_LIMIT: int = 10
    REGISTER_RATE_LIMIT: int = 5
    REFRESH_RATE_LIMIT: int = 30

    @property
    def access_token_expire_seconds(self) -> int:
        return self.ACCESS_TOKEN_EXPIRE_MINUTES * 60

    @property
    def refresh_token_expire_seconds(self) -> int:
        return self.REFRESH_TOKEN_EXPIRE_MINUTES * 60

    @computed_field  # type: ignore[prop-decorator]
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.DB_USER}:"
            f"{quote_plus(self.DB_PASSWORD)}"
            f"@{self.DB_HOST}:{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )


settings = Settings()  # type: ignore[call-arg]
