from pydantic import BaseModel, Field

class UserRegistrationRequest(BaseModel):
    username: str
    email: str
    password: str
    phoneNumber: int = Field(min_length=10, max_length=10)