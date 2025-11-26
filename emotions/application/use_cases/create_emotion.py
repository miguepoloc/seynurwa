"""Create emotion use case."""

from uuid import UUID

from emotions.application.dtos.create_emotion_dto import CreateEmotionDTO
from emotions.application.dtos.emotion_dto import EmotionDTO
from emotions.domain.entities.emotion import Emotion


class CreateEmotion:
    """Create emotion use case."""
    
    def __init__(self, emotion_repository):
        """Initialize with repositories."""
        self.emotion_repository = emotion_repository
    
    def execute(self, user_id: UUID, data: CreateEmotionDTO) -> EmotionDTO:
        """Execute emotion creation.
        
        Args:
            user_id: Current authenticated user ID
            data: Emotion data with AI response
            
        Returns:
            EmotionDTO with created emotion
        """
        # Create emotion entity
        emotion = Emotion(
            user_id=user_id,
            title=data.title,
            text=data.text,
            ai_response=data.ai_response
        )
        
        # Save emotion
        created_emotion = self.emotion_repository.create(emotion)
        
        # Return DTO
        return EmotionDTO(
            id=created_emotion.id,
            title=created_emotion.title,
            text=created_emotion.text,
            ai_response=created_emotion.ai_response,
            created_at=created_emotion.created_at
        )
