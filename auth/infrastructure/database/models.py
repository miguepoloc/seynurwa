"""Database models."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from common.infrastructure.database.base import Base


class UserModel(Base):
    """User database model."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
