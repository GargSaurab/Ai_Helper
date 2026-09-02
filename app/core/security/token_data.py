from datetime import datetime

from pydantic import BaseModel, ConfigDict

class TokenData(BaseModel):
    user_id: str | None = None
    email: str | None = None
    jti: str | None = None         # JWT ID (essential for revocation/blacklisting)
    iat: datetime | int | None = None  # Issued At
    exp: datetime | int | None = None  # Expiration time

    # Makes the model immutable
    model_config = ConfigDict(frozen=True)