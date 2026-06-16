from pydantic import BaseModel, EmailStr, Field


class UserRegistrationRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)

    email: EmailStr

    password: str = Field(min_length=8, max_length=128)

    phone_number: str | None = Field(
        default=None,
        min_length=10,
        max_length=10,
    )
