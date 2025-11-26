"""Emotion entity."""

from datetime import datetime
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field


def colombia_now() -> datetime:
    """Get current datetime in Colombia timezone."""
    return datetime.now(ZoneInfo("America/Bogota"))


class Emotion(BaseModel):
    """Emotion domain entity."""
    
    user_id: UUID
    title: str
    text: str
    ai_response: str
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=colombia_now)
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
