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
