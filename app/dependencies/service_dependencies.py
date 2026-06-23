from typing import Annotated

from fastapi import Depends

from app.dependencies.repo_dependencies import UserRepositoryDep
from app.services.user_service import UserService


def get_user_service(user_repo: UserRepositoryDep) -> UserService:
    return UserService(user_repo)


UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
]
