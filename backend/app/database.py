from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

SQLALCHEMY_DATABASE_URL = "sqlite:///./biblioteca.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()