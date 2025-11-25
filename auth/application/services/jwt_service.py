"""JWT service for token operations."""

import os
from datetime import datetime, timedelta
from uuid import UUID

import jwt


class JWTService:
    """Handle JWT token operations."""
    
    def __init__(self):
        """Initialize with environment variables."""
        self.secret_key = os.getenv("JWT_SECRET", "change-me-in-production")
        self.expiration_hours = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
        self.algorithm = "HS256"
    
    def generate_token(self, user_id: UUID, email: str) -> tuple[str, int]:
        """Generate JWT token.
        
        Returns:
            Tuple of (token, expires_in_seconds)
        """
        expires_in = self.expiration_hours * 3600
        expiration = datetime.utcnow() + timedelta(hours=self.expiration_hours)
        
        payload = {
            "sub": str(user_id),
            "email": email,
            "exp": expiration,
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token, expires_in
    
    def validate_token(self, token: str) -> dict | None:
        """Validate and decode JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
