"""Login DTO."""

from pydantic import BaseModel, EmailStr


class LoginDTO(BaseModel):
    """Login credentials."""
    
    email: EmailStr
    password: str
