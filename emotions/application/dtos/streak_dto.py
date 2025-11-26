"""Streak DTO."""

from datetime import date

from pydantic import BaseModel


class StreakDTO(BaseModel):
    """Output DTO for user's emotion streak."""
    
    has_emotion_today: bool
    current_streak: int
    last_emotion_date: date | None = None
