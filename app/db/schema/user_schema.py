from datetime import datetime, timezone

from sqlalchemy import Index, text
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (Index("uq_users_email_lower", text("lower(email)"), unique=True),)
    id: int | None = Field(default=None, primary_key=True)

    name: str

    email: str

    phone_number: str | None = Field(default=None, index=True, unique=True)

    password_hash: str

    email_verified: bool = Field(default=False)

    phone_verified: bool = Field(default=False)

    is_logged_out: bool = Field(default=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
