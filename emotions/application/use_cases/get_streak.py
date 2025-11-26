"""Get streak use case."""

from datetime import date, timedelta, datetime
from uuid import UUID
from zoneinfo import ZoneInfo

from emotions.application.dtos.streak_dto import StreakDTO

COLOMBIA_TZ = ZoneInfo("America/Bogota")


class GetStreak:
    """Get emotion streak for user."""
    
    def __init__(self, emotion_repository):
        """Initialize with repository."""
        self.emotion_repository = emotion_repository
    
    def execute(self, user_id: UUID) -> StreakDTO:
        """Calculate user's emotion streak.
        
        Args:
            user_id: Current authenticated user ID
            
        Returns:
            StreakDTO with streak information
        """
        # Get today's date in Colombia timezone
        today = datetime.now(COLOMBIA_TZ).date()
        
        # Check if user has emotion today
        has_today = self.emotion_repository.has_emotion_on_date(user_id, today)
        
        # Get all dates when user created emotions
        emotion_dates = self.emotion_repository.get_emotion_dates_for_user(user_id)
        
        if not emotion_dates:
            return StreakDTO(
                has_emotion_today=False,
                current_streak=0,
                last_emotion_date=None
            )
        
        # Calculate streak
        current_streak = 0
        check_date = today if has_today else today - timedelta(days=1)
        
        for emotion_date in emotion_dates:
            if emotion_date == check_date:
                current_streak += 1
                check_date -= timedelta(days=1)
            elif emotion_date < check_date:
                # Gap found, streak broken
                break
        
        return StreakDTO(
            has_emotion_today=has_today,
            current_streak=current_streak,
            last_emotion_date=emotion_dates[0] if emotion_dates else None
        )
