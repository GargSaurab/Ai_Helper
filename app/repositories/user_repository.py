from sqlmodel import Session, select

from app.db.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db
