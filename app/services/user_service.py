from fastapi import HTTPException, status

from app.core.logging.logger import get_logger
from app.core.password_hasher import hash_password, verify_password
from app.db.repositories.user_repository import UserRepository
from app.db.schema.user_schema import User
from app.models.request.user_login_request import UserLoginRequest
from app.models.request.user_registration_request import UserRegistrationRequest
from app.models.response.base_response import BaseResponse

LOG = get_logger(__name__)


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, request: UserRegistrationRequest):

        LOG.info(
            "Registration requested for email: %s",
            request.email,
        )

        if self.user_repo.get_user_by_email(request.email):
            LOG.warning(
                "Registration failed. Email already exists: %s",
                request.email,
            )

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        if self.user_repo.get_user_by_phone_number(request.phone_number):
            LOG.warning(
                "Registration failed. Phone number already exists: %s",
                request.phone_number,
            )

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this phone already exists",
            )

        user = User(
            name=request.username,
            email=request.email,
            password_hash=hash_password(request.password),
            phone_number=request.phone_number,
        )

        saved_user = self.user_repo.save(user)

        if not saved_user:
            LOG.error(
                "Registration failed. Repository returned None for email: %s",
                request.email,
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User registration failed. Please try again.",
            )

        LOG.info(
            "User registered successfully. User ID: %s",
            saved_user.id,
        )

        return {
            "id": saved_user.id,
            "name": saved_user.name,
            "email": saved_user.email,
            "phone_number": saved_user.phone_number,
        }

    def login(self, request: UserLoginRequest) -> BaseResponse:

        LOG.info(
            "Login requested for email: %s",
            request.email,
        )

        user: User | None = self.user_repo.get_user_by_email(request.email)

        if not user:
            LOG.warning(
                "Login failed. User not found: %s",
                request.email,
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email does not exist",
            )

        if not verify_password(request.password, user.password_hash):
            LOG.warning(
                "Login failed. Invalid password for user ID: %s",
                user.id,
            )

            return BaseResponse(
                code=401,
                message="Invalid email or password",
            )

        LOG.info(
            "User logged in successfully. User ID: %s",
            user.id,
        )

        return BaseResponse(
            code=200,
            message="Login Successful",
        )
