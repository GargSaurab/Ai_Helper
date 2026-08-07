from app.core.exception.app_exception import AppException
from app.core.exception.error_codes import ErrorCodes
from app.core.logging.logger import get_logger
from app.core.security.password_hasher import hash_password, verify_password
from app.core.security.token_data import TokenData
from app.db.repositories.user_repository import UserRepository
from app.db.schema.user_schema import User
from app.models.request.user_login_request import UserLoginRequest
from app.models.request.user_registration_request import UserRegistrationRequest
from app.core.security.jwt_service import JWTService

from sqlalchemy.exc import SQLAlchemyError

LOG = get_logger(__name__)

class UserService:
    def __init__(self, user_repo: UserRepository, jwt_service: JWTService):
        self.user_repo = user_repo
        self.jwt_service = jwt_service

    def register(self, request: UserRegistrationRequest) -> str:

        LOG.info(
            "Registration requested for email: %s",
            request.email,
        )

        if self.user_repo.get_user_by_email(request.email):
            raise AppException(ErrorCodes.ALREADY_EXISTS, "Email already Exists")

        if self.user_repo.get_user_by_phone_number(request.phone_number):
            raise AppException(ErrorCodes.ALREADY_EXISTS, "Phone Number already Exists")

        user = User(
            name=request.username,
            email=request.email,
            password_hash=hash_password(request.password),
            phone_number=request.phone_number,
        )

        try:
            saved_user = self.user_repo.save(user)

        except SQLAlchemyError as ex:
            raise AppException(ErrorCodes.USER_REGISTRATION_FAILED) from ex

        LOG.info(
            "User registered successfully. User ID: %s",
            saved_user.id,
        )

        return self._generate_access_token(saved_user)

    def login(self, request: UserLoginRequest) -> str:

        LOG.info(
            "Login requested for email: %s",
            request.email
        )

        user: User | None = self.user_repo.get_user_by_email(request.email)

        if user is None:
            raise AppException(ErrorCodes.NOT_FOUND, "User Not Found")

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise AppException(ErrorCodes.INVALID_REQUEST, "Invalid Credentials")

        LOG.info(
            "User logged in successfully. User ID: %s",
            user.id,
        )

        return self._generate_access_token(user)
    
    def _generate_access_token(self, user: User) -> str:
        return self.jwt_service.encode(
            TokenData(
                user_id=str(user.id),
                email=user.email,
            )
        )
