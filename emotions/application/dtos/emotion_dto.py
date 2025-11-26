"""Emotion DTO."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EmotionDTO(BaseModel):
    """Output DTO for emotion with user info."""
    
    id: UUID
    title: str
    text: str
    ai_response: str
    created_at: datetime
