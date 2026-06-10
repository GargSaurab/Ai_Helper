from app.services.user_service import UserService
from app.db import engine
from fastapi import Depends
from typing import Annotated
from sqlmodel import Session

userServiceDep = Annotated[UserService, Depends(UserService)]

# Code above omitted 👆

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]