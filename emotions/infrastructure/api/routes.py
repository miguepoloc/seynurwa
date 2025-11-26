"""FastAPI routes for emotions."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from common.infrastructure.auth.jwt_auth import AuthenticatedUser
from common.infrastructure.database.session import get_db_session
from emotions.application.dtos.create_emotion_dto import CreateEmotionDTO
from emotions.application.dtos.emotion_dto import EmotionDTO
from emotions.application.dtos.streak_dto import StreakDTO
from emotions.application.use_cases.create_emotion import CreateEmotion
from emotions.application.use_cases.list_emotions import ListEmotions
from emotions.application.use_cases.get_streak import GetStreak
from emotions.infrastructure.database.repository import EmotionRepository

# Router
router = APIRouter()


@router.post("", response_model=EmotionDTO, status_code=status.HTTP_201_CREATED)
def create_emotion(
    data: CreateEmotionDTO,
    current_user: AuthenticatedUser,
    session: Session = Depends(get_db_session)
):
    """Create emotion for authenticated user.
    
    Requires JWT bearer token in Authorization header.
    Includes user's emotion text and AI response.
    """
    try:
        emotion_repo = EmotionRepository(session)
        use_case = CreateEmotion(emotion_repo)
        return use_case.execute(current_user.id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=list[EmotionDTO])
def list_emotions(
    current_user: AuthenticatedUser,
    session: Session = Depends(get_db_session)
):
    """List all emotions for authenticated user.
    
    Returns emotions ordered by creation date (newest first).
    Requires JWT bearer token in Authorization header.
    """
    emotion_repo = EmotionRepository(session)
    use_case = ListEmotions(emotion_repo)
    return use_case.execute(current_user.id)


@router.get("/streak", response_model=StreakDTO)
def get_streak(
    current_user: AuthenticatedUser,
    session: Session = Depends(get_db_session)
):
    """Get emotion streak for authenticated user.
    
    Returns:
    - has_emotion_today: whether user created emotion today
    - current_streak: number of consecutive days with emotions
    - last_emotion_date: date of most recent emotion
    
    Requires JWT bearer token in Authorization header.
    """
    emotion_repo = EmotionRepository(session)
    use_case = GetStreak(emotion_repo)
    return use_case.execute(current_user.id)
