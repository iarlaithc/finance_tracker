# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os
from dotenv import load_dotenv

#load environmental variables
load_dotenv()

# Get database URL from environment variable or use default SQLite
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./finance.db"
)

# Ensure the data directory exists
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    db_path = Path(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", ""))
    db_path.parent.mkdir(parents=True, exist_ok=True)

# Create engine
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

def cleanup_db():
    Base.metadata.drop_all(bind=engine)