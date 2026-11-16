from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.utils import normalize_string


class UserRegistrationRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)

    email: EmailStr

    @field_validator("email")
    @classmethod
    def canonicalize_email(cls, email: EmailStr) -> str:
        return normalize_string(str(email))

    password: str = Field(min_length=8, max_length=128)

    phone_number: str | None = Field(
        default=None,
        min_length=10,
        max_length=10,
    )
