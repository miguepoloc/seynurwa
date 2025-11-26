"""JWT authentication dependency for FastAPI."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from auth.application.services.jwt_service import JWTService

# HTTP Bearer token scheme
security = HTTPBearer()


class CurrentUser(BaseModel):
    """Current authenticated user info from JWT."""
    
    id: UUID
    email: str


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> CurrentUser:
    """Extract and validate current user from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials from request header
        
    Returns:
        CurrentUser with id and email
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    
    # Validate token
    jwt_service = JWTService()
    payload = jwt_service.validate_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user info from payload
    try:
        user_id = UUID(payload.get("sub"))
        email = payload.get("email")
        
        if not user_id or not email:
            raise ValueError("Missing user info in token")
            
        return CurrentUser(id=user_id, email=email)
    except (ValueError, KeyError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token payload: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Type alias for dependency injection
AuthenticatedUser = Annotated[CurrentUser, Depends(get_current_user)]
