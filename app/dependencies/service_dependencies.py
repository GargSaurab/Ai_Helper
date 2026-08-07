from typing import Annotated

from fastapi import Depends

from app.dependencies.repo_dependencies import UserRepositoryDep
from app.services.user_service import UserService
from app.core.security.security_dependency import JWTServiceDep

def get_user_service(user_repo: UserRepositoryDep, jwtService : JWTServiceDep) -> UserService:
    return UserService(user_repo, jwtService        )


UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service)
]
