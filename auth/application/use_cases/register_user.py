"""Register user use case."""

from auth.application.dtos.register_dto import RegisterDTO
from auth.application.dtos.user_dto import UserDTO
from auth.domain.entities.user import User
from auth.domain.exceptions.auth_errors import UserAlreadyExistsError
from auth.domain.value_objects.email import Email
from auth.domain.value_objects.password import HashedPassword


class RegisterUser:
    """Register a new user."""
    
    def __init__(self, repository):
        """Initialize with repository."""
        self.repository = repository
    
    def execute(self, data: RegisterDTO) -> UserDTO:
        """Execute registration."""
        # Create email value object
        email = Email(value=data.email)
        
        # Check if user exists
        if self.repository.exists_by_email(email.value):
            raise UserAlreadyExistsError(email.value)
        
        # Hash password
        hashed_password = HashedPassword.from_plain(data.password)
        
        # Create user entity
        user = User(
            name=data.name,
            email=email,
            hashed_password=hashed_password
        )
        
        # Save user
        created_user = self.repository.create(user)
        
        # Return DTO
        return UserDTO(
            id=created_user.id,
            name=created_user.name,
            email=created_user.email.value,
            created_at=created_user.created_at
        )
