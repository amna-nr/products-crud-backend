from app.core.config import settings 
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import Annotated
from fastapi import Depends


DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=settings.ENVIRONMENT == "development")

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autoflush=False)

def get_db():
    with SessionLocal as db:
        yield db

db_dependency = Annotated[Session, Depends(get_db)]