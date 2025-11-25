"""User entity."""

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from auth.domain.value_objects.email import Email
from auth.domain.value_objects.password import HashedPassword


class User(BaseModel):
    """User domain entity."""
    
    name: str
    email: Email
    hashed_password: HashedPassword
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
    
    def verify_password(self, plain_password: str) -> bool:
        """Verify password against stored hash."""
        return self.hashed_password.verify(plain_password)
