from sqlalchemy import func
from sqlmodel import Session, select

from app.core.utils import normalize_string
from app.db.schema.user_schema import User

from sqlalchemy.exc import SQLAlchemyError


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

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
        try:
            user.email = normalize_string(user.email)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            return user

        except SQLAlchemyError:
            self.db.rollback()
            raise
