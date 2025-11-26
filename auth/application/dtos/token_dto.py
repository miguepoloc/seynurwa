"""Token DTO."""

from pydantic import BaseModel


class TokenDTO(BaseModel):
    """JWT token response."""
    
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    name: str
