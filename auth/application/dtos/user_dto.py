"""User response DTO."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    """User data for responses."""
    
    id: UUID
    name: str
    email: EmailStr
    created_at: datetime
