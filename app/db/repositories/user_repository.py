from sqlmodel import Session, select

from app.db.schema.user_schema import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db
        
    def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        return self.db.exec(statement).first()

    def get_user_by_phone_number(self, phone_number: str) -> User | None:
        statement = select(User).where(User.phone_number == phone_number)

        return self.db.exec(statement).first()
    
    

