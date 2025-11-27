from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://biblioteca_user:senha_segura123@db:5432/biblioteca_digital"
) #docker postgres

SQLALCHEMY_DATABASE_URL = "sqlite:///./biblioteca.db" #local sqlitecom uvicorn

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