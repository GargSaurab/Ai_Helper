from sqlmodel import Session, create_engine
from fastapi import Depends
from typing import Annotated
from app.core.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # False in production
)


def get_session() -> Session:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
