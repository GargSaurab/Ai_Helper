from datetime import datetime, timezone

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str

    email: str = Field(index=True, unique=True)

    phone_number: str = Field(index=True, unique=True)

    password_hash: str

    email_verified: bool = Field(default=False)

    phone_verified: bool = Field(default=False)

    is_logged_out: bool = Field(default=False)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )