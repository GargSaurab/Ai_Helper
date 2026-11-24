from typing import Annotated

from fastapi import Depends

from app.db.db_session import SessionDep
from app.db.repositories.user_repository import UserRepository
from app.db.transaction_manager import TransactionManagerDep


def get_user_repo(
    db: SessionDep, transactions: TransactionManagerDep
) -> UserRepository:  # type: ignore
    return UserRepository(db, transactions)


UserRepositoryDep = Annotated[
    UserRepository,
    Depends(get_user_repo),
]
