"""FastAPI routes for authentication."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.application.dtos.login_dto import LoginDTO
from auth.application.dtos.register_dto import RegisterDTO
from auth.application.dtos.token_dto import TokenDTO
from auth.application.dtos.user_dto import UserDTO
from auth.application.services.jwt_service import JWTService
from auth.application.use_cases.login_user import LoginUser
from auth.application.use_cases.register_user import RegisterUser
from auth.domain.exceptions.auth_errors import (
    UserAlreadyExistsError,
    InvalidCredentialsError
)
from auth.infrastructure.database.repository import UserRepository
from common.infrastructure.database.session import get_db_session

# Router
router = APIRouter()


@router.post("/register", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterDTO,
    session: Session = Depends(get_db_session)
):
    """Register a new user."""
    try:
        repository = UserRepository(session)
        use_case = RegisterUser(repository)
        return use_case.execute(data)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{e.email}' already exists"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenDTO)
def login(
    data: LoginDTO,
    session: Session = Depends(get_db_session)
):
    """Login and get JWT token."""
    try:
        repository = UserRepository(session)
        jwt_service = JWTService()
        use_case = LoginUser(repository, jwt_service)
        return use_case.execute(data)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
