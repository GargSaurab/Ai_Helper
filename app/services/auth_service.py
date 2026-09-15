import uuid

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
from app.core.redis.redis_service import RedisService
from app.core.config import settings

from sqlalchemy.exc import SQLAlchemyError

LOG = get_logger(__name__)


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        jwt_service: JWTService,
        redis_service: RedisService,
    ):
        self.user_repo = user_repo
        self.jwt_service = jwt_service
        self.redis_service = redis_service

    access_token_expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    refresh_token_expire_minutes: int = settings.REFRESH_TOKEN_EXPIRE_MINUTES

    def register(self, request: UserRegistrationRequest) -> dict:

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

        return self._generate_token_dict(saved_user)

    def login(self, request: UserLoginRequest) -> str:

        LOG.info("Login requested for email: %s", request.email)

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

        return self._generate_token_dict(user)

    def _generate_token_dict(self, user: User) -> dict[str, str]:

        refresh_jti = str(uuid.uuid4())

        access_token = self.jwt_service.encode(
            TokenData(user_id=str(user.id), email=user.email),
            expiry_time=self.access_token_expire_minutes,
        )

        refresh_token = self.jwt_service.encode(
            TokenData(
                user_id=str(user.id),
                email=user.email,
            ),
            expiry_time=self.refresh_token_expire_minutes,
            extra_claims={"jti": refresh_jti},
        )

        redis_key = f"refresh_token:{user.id}:{refresh_jti}"
        self.redis_service.set(
            key=redis_key,
            value="active",
            ttl_seconds=settings.refresh_token_expire_seconds,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def rotate_refresh_token(self, refresh_token_str: str) -> dict[str, str]:
        LOG.info("Refresh token rotation requested")

        # 1. Decode refresh token claims
        claims = self.jwt_service.decode(refresh_token_str)

        redis_key = f"refresh_token:{claims.user_id}:{claims.jti}"

        # 2. Check existence in Redis
        if not self.redis_service.exists(redis_key):
            LOG.warning(
                "Refresh token not found or already revoked for user_id: %s, jti: %s",
                claims.user_id,
                claims.jti,
            )
            raise AppException(
                ErrorCodes.UNAUTHORIZED, "Refresh token expired or revoked"
            )

        # 3. Single-Use Rotation: Invalidate previous refresh token
        self.redis_service.delete(redis_key)
        LOG.info(
            "Previous refresh token revoked for user_id: %s, jti: %s",
            claims.user_id,
            claims.jti,
        )

        # 4. Fetch user
        user = self.user_repo.get_user_by_email(claims.email)
        if not user:
            LOG.error(
                "User associated with valid token no longer exists in DB: user_id=%s",
                claims.user_id,
            )
            raise AppException(ErrorCodes.NOT_FOUND, "User not found")

        LOG.info("New token pair successfully minted for user_id: %s", user.id)
        return self._generate_token_dict(user)

    def logout_current_session(self, refresh_token_str: str) -> None:
        """Revokes the specific refresh token session presented by the client."""
        LOG.info("Single device logout requested")
        claims = self.jwt_service.decode(refresh_token_str)

        redis_key = f"refresh_token:{claims.user_id}:{claims.jti}"
        deleted_count = self.redis_service.delete(redis_key)

        LOG.info(
            "Session revoked for user_id: %s, jti: %s (keys removed: %d)",
            claims.user_id,
            claims.jti,
            deleted_count,
        )

    def logout_all_devices(self, user_id: str) -> None:
        """Invalidates all active refresh token sessions for a user across all devices."""
        LOG.info("Global logout requested for all devices: user_id=%s", user_id)
        pattern = f"refresh_token:{user_id}:*"
        deleted_count = self.redis_service.delete_pattern(pattern)
        LOG.info(
            "All sessions revoked for user_id: %s (total keys cleared: %d)",
            user_id,
            deleted_count,
        )
