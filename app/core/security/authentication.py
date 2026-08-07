from typing import Annotated

from fastapi import Depends, FastAPI

from app.core.exception.app_exception import AppException
from app.core.exception.error_codes import ErrorCodes
from app.core.security.jwt_service import JWTService
from app.db.repositories.user_repository import UserRepository
from app.db.schema.user_schema import User
from app.models.response.user_response import UserResponse

app = FastAPI()

class AuthenticationService:

    def __init__(
        self,
        jwt_service: JWTService,
        user_repo: UserRepository,
    ):
        self.jwt_service = jwt_service
        self.user_repo = user_repo

    async def get_current_user(
        self,
        token: str,
    ) -> UserResponse:

        claims = self.jwt_service.decode(token)

        user = self.user_repo.get_user_by_email(
            claims.email
        )

        if user is None:
            raise AppException(
                ErrorCodes.NOT_FOUND,
                "User not found",
            )

        return UserResponse.model_validate(user)