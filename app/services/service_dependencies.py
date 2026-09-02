from typing import Annotated

from fastapi import Depends

from app.db.repo_dependencies import UserRepositoryDep
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.core.security.security_dependency import JWTServiceDep
from app.core.redis.redis_dependency import RedisServiceDep

def get_user_service(user_repo: UserRepositoryDep, jwt_service : JWTServiceDep) -> UserService:
    return UserService(user_repo, jwt_service)

def get_auth_service(user_repo: UserRepositoryDep, jwt_service : JWTServiceDep, redis_service : RedisServiceDep) -> AuthService:
    return AuthService(user_repo, jwt_service, redis_service)

UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service)
]

AuthServiceDep = Annotated[
    AuthService,
    Depends(get_auth_service)
]
