"""Authentication domain exceptions."""


class AuthError(Exception):
    """Base auth exception."""
    pass


class UserAlreadyExistsError(AuthError):
    """User with this email already exists."""
    
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email '{email}' already exists")


class InvalidCredentialsError(AuthError):
    """Invalid login credentials."""
    
    def __init__(self):
        super().__init__("Invalid email or password")


class UserNotFoundError(AuthError):
    """User not found."""
    
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User not found: {email}")
