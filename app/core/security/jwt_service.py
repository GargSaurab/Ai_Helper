from datetime import datetime, timedelta, timezone
from typing import Any, Optional
import jwt

from app.core.config import settings
from app.core.security.token_data import TokenData
from app.core.exception.app_exception import AppException
from app.core.exception.error_codes import ErrorCodes


class JWTService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM

    def encode(
        self,
        token_data: TokenData,
        expiry_time: int,
        extra_claims: dict[str, Any] | None = None,
    ) -> str:

        payload = token_data.model_dump(exclude_none=True)

        if extra_claims:
            for key, value in extra_claims.items():
                if key not in payload:
                    payload[key] = value

        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=expiry_time)

        payload.update(
            {
                "iat": int(now.timestamp()),
                "exp": int(expire.timestamp()),
            }
        )

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def decode(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
            return TokenData(**payload)
        except jwt.ExpiredSignatureError:
            raise AppException(
                error_code=ErrorCodes.TOKEN_EXPIRED,
                status_code=401,
                detail="Token has expired",
            )
        except jwt.InvalidTokenError:
            raise AppException(
                error_code=ErrorCodes.INVALID_TOKEN,
                status_code=401,
                detail="Invalid token signature or format",
            )
