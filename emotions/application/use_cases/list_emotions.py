"""List emotions use case."""

from uuid import UUID

from emotions.application.dtos.emotion_dto import EmotionDTO


class ListEmotions:
    """List all emotions for user use case."""
    
    def __init__(self, emotion_repository):
        """Initialize with repositories."""
        self.emotion_repository = emotion_repository
    
    def execute(self, user_id: UUID) -> list[EmotionDTO]:
        """List all emotions for user ordered by created_at desc.
        
        Args:
            user_id: Current authenticated user ID
            
        Returns:
            List of EmotionDTO ordered by creation date (newest first)
        """
        # Find all emotions
        emotions = self.emotion_repository.find_all_by_user(user_id)
        
        # Convert to DTOs
        return [
            EmotionDTO(
                id=emotion.id,
                title=emotion.title,
                text=emotion.text,
                ai_response=emotion.ai_response,
                created_at=emotion.created_at
            )
            for emotion in emotions
        ]
