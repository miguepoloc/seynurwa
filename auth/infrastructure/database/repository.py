"""Add find_by_id method to UserRepository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.domain.entities.user import User
from auth.domain.value_objects.email import Email
from auth.domain.value_objects.password import HashedPassword
from auth.infrastructure.database.models import UserModel


class UserRepository:
    """User repository with database operations."""
    
    def __init__(self, session: Session):
        """Initialize with database session."""
        self.session = session
    
    def exists_by_email(self, email: str) -> bool:
        """Check if user exists with given email."""
        stmt = select(UserModel).where(UserModel.email == email)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    def find_by_id(self, user_id: UUID) -> User | None:
        """Find user by ID."""
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        return User(
            name=model.name,
            email=Email(value=model.email),
            hashed_password=HashedPassword(value=model.hashed_password),
            id=model.id,
            created_at=model.created_at
        )
    
    def find_by_email(self, email: str) -> User | None:
        """Find user by email."""
        stmt = select(UserModel).where(UserModel.email == email)
        result = self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        # Map to domain entity
        return User(
            name=model.name,
            email=Email(value=model.email),
            hashed_password=HashedPassword(value=model.hashed_password),
            id=model.id,
            created_at=model.created_at
        )
    
    def create(self, user: User) -> User:
        """Create new user."""
        model = UserModel(
            id=user.id,
            name=user.name,
            email=user.email.value,
            hashed_password=user.hashed_password.value,
            created_at=user.created_at
        )
        
        self.session.add(model)
        self.session.flush()
        self.session.refresh(model)
        
        # Map back to domain entity
        return User(
            name=model.name,
            email=Email(value=model.email),
            hashed_password=HashedPassword(value=model.hashed_password),
            id=model.id,
            created_at=model.created_at
        )
