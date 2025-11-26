"""Get today's emotion use case."""

from datetime import date
from uuid import UUID

from emotions.application.dtos.emotion_dto import EmotionDTO
from emotions.domain.exceptions.emotion_errors import EmotionNotFound


class GetTodayEmotion:
    """Get today's emotion use case."""
    
    def __init__(self, emotion_repository, user_repository):
        """Initialize with repositories."""
        self.emotion_repository = emotion_repository
        self.user_repository = user_repository
    
    def execute(self, user_id: UUID) -> EmotionDTO:
        """Get today's emotion for user.
        
        Args:
            user_id: Current authenticated user ID
            
        Returns:
            EmotionDTO with today's emotion
            
        Raises:
            EmotionNotFound: If no emotion found for today
        """
        today = date.today()
        
        # Find emotion for today
        emotion = self.emotion_repository.find_by_user_and_date(user_id, today)
        
        if not emotion:
            raise EmotionNotFound(str(user_id), str(today))
        
        # Get user info
        user = self.user_repository.find_by_id(user_id)
        user_name = user.name if user else "Unknown"
        
        # Return DTO
        return EmotionDTO(
            id=emotion.id,
            user_name=user_name,
            title=emotion.title,
            text=emotion.text,
            date=emotion.date,
            created_at=emotion.created_at
        )
