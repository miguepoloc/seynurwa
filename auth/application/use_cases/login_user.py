"""Login user use case."""

from auth.application.dtos.login_dto import LoginDTO
from auth.application.dtos.token_dto import TokenDTO
from auth.application.services.jwt_service import JWTService
from auth.domain.exceptions.auth_errors import InvalidCredentialsError
from auth.domain.value_objects.email import Email


class LoginUser:
    """Login user and generate token."""
    
    def __init__(self, repository, jwt_service: JWTService):
        """Initialize with repository and JWT service."""
        self.repository = repository
        self.jwt_service = jwt_service
    
    def execute(self, data: LoginDTO) -> TokenDTO:
        """Execute login."""
        # Create email value object
        email = Email(value=data.email)
        
        # Find user
        user = self.repository.find_by_email(email.value)
        if not user:
            raise InvalidCredentialsError()
        
        # Verify password
        if not user.verify_password(data.password):
            raise InvalidCredentialsError()
        
        # Generate token
        token, expires_in = self.jwt_service.generate_token(
            user_id=user.id,
            email=user.email.value
        )
        
        return TokenDTO(
            access_token=token,
            token_type="bearer",
            expires_in=expires_in
        )
