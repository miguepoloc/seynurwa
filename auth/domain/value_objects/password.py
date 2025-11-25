"""Password value object with hashing."""

import bcrypt

from pydantic import BaseModel


class HashedPassword(BaseModel):
    """Hashed password value object."""
    
    value: str
    
    class Config:
        """Pydantic configuration."""
        frozen = True
    
    def verify(self, plain_password: str) -> bool:
        """Verify plain password against hash."""
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                self.value.encode('utf-8')
            )
        except Exception:
            return False
    
    @staticmethod
    def from_plain(plain_password: str) -> 'HashedPassword':
        """Create hashed password from plain text."""
        if len(plain_password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return HashedPassword(value=hashed.decode('utf-8'))
