from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.db.db_session import SessionDep

class TransactionManager:
    """Controls the transaction for repositories sharing one request session."""

    def __init__(self, session: Session):
        self._session = session

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()


def get_transaction_manager(session: SessionDep) -> TransactionManager:  # type: ignore
    return TransactionManager(session)


TransactionManagerDep = Annotated[
    TransactionManager,
    Depends(get_transaction_manager),
]
