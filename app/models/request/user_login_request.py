from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.utils import normalize_string


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def canonicalize_email(cls, email: EmailStr) -> str:
        return normalize_string(str(email))
