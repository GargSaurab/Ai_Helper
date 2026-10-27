from app.core.logging.logger import get_logger
from app.db.repositories.user_repository import UserRepository
from app.core.security.jwt_service import JWTService


LOG = get_logger(__name__)


class UserService:
    def __init__(self, user_repo: UserRepository, jwt_service: JWTService):
        self.user_repo = user_repo
        self.jwt_service = jwt_service
