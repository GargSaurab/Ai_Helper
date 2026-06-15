from typing import Annotated

from fastapi import Depends

from app.db.db_session import SessionDep
from app.db.repositories.user_repository import UserRepository


def get_user_repo(db: SessionDep) -> UserRepository: # type: ignore
    return UserRepository(db)


UserRepositoryDep = Annotated[
    UserRepository,
    Depends(get_user_repo),
]