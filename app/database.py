from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from sqlmodel import SQLModel


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    print("Creating tables:", SQLModel.metadata.tables.keys())  # Debug print
    SQLModel.metadata.create_all(bind=engine)

def get_db():
    return SessionLocal()
