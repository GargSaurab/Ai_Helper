from pydantic import BaseModel, ConfigDict

class TokenData(BaseModel):
    user_id: str | None = None
    email: str | None = None

    # Makes the model immutable
    model_config = ConfigDict(frozen=True)