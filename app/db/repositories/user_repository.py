from sqlalchemy import func
from sqlmodel import Session, select

from app.core.utils import normalize_string
from app.db.schema.user_schema import User
from app.db.transaction_manager import TransactionManager


class UserRepository:
    def __init__(self, db: Session, transactions: TransactionManager):
        self.db = db
        self.transactions = transactions

    def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(func.lower(User.email) == normalize_string(email))

        return self.db.exec(statement).first()

    def get_user_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.db.exec(statement).first()

    def get_user_by_phone_number(self, phone_number: str | None) -> User | None:
        if phone_number is None:
            return None

        statement = select(User).where(User.phone_number == phone_number)

        return self.db.exec(statement).first()

    def save(self, user: User) -> User:
        user.email = normalize_string(user.email)
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user
