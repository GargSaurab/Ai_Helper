from dataclasses import asdict

import jwt

from app.core.config import settings
from app.core.security.token_data import TokenData


class JWTService:

    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM

    def encode(self, token_data: TokenData) -> str:
        return jwt.encode(
            token_data.model_dump(),
            self.secret_key,
            algorithm=self.algorithm,
        )

    def decode(self, token: str) -> TokenData:

        payload = jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
        )

        return TokenData(**payload)