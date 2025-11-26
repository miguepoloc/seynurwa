"""Create emotion DTO."""

from pydantic import BaseModel, Field


class CreateEmotionDTO(BaseModel):
    """Input DTO for creating an emotion."""
    
    title: str = Field(..., min_length=1, max_length=100, description="Emotion title")
    text: str 
    ai_response: str
