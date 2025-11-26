"""Database session management."""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Lazy engine initialization
_engine = None
_SessionLocal = None


def get_engine():
    """Get or create database engine."""
    global _engine, _SessionLocal
    if _engine is None:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is not set")
        _engine = create_engine(database_url, echo=False)
        _SessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False)
    return _engine, _SessionLocal


def get_db_session() -> Generator[Session, None, None]:
    """Get database session dependency for FastAPI."""
    _, SessionLocal = get_engine()
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
