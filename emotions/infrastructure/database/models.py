"""Emotion database model."""

from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from common.infrastructure.database.base import Base

COLOMBIA_TZ = ZoneInfo("America/Bogota")


def colombia_now() -> datetime:
    """Get current datetime in Colombia timezone."""
    return datetime.now(COLOMBIA_TZ)


class EmotionModel(Base):
    """Emotion database model."""
    
    __tablename__ = "emotions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=colombia_now, nullable=False)
    
    @property
    def created_at_colombia(self) -> datetime:
        """Get created_at converted to Colombia timezone."""
        if self.created_at.tzinfo is None:
            # If naive datetime, assume UTC
            return self.created_at.replace(tzinfo=ZoneInfo("UTC")).astimezone(COLOMBIA_TZ)
        return self.created_at.astimezone(COLOMBIA_TZ)
