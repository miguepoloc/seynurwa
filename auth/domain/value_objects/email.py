"""Email value object."""

import re

from pydantic import BaseModel, validator


class Email(BaseModel):
    """Email value object with validation."""
    
    value: str
    
    class Config:
        """Pydantic configuration."""
        frozen = True
    
    @validator('value')
    def validate_email(cls, v):
        """Validate email format."""
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not v or not pattern.match(v):
            raise ValueError(f"Invalid email format: {v}")
        return v
    
    def __str__(self) -> str:
        return self.value
