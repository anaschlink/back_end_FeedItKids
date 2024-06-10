import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

db_password = os.getenv("SENHA_BANCO")

SQLALCHEMY_DATABASE_URL = f"postgresql://avnadmin:{db_password}@pg-25cb39a-abnschlink-031a.h.aivencloud.com:22352/db_fitKids?sslmode=require"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}, future=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future= True)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()