"""Emotion repository implementation."""

from datetime import date
from uuid import UUID

from sqlalchemy import select, and_, func, desc
from sqlalchemy.orm import Session

from emotions.domain.entities.emotion import Emotion
from emotions.infrastructure.database.models import EmotionModel


class EmotionRepository:
    """Emotion repository with database operations."""
    
    def __init__(self, session: Session):
        """Initialize with database session."""
        self.session = session
    
    def create(self, emotion: Emotion) -> Emotion:
        """Create new emotion."""
        model = EmotionModel(
            id=emotion.id,
            user_id=emotion.user_id,
            title=emotion.title,
            text=emotion.text,
            ai_response=emotion.ai_response,
            created_at=emotion.created_at
        )
        
        self.session.add(model)
        self.session.flush()
        self.session.refresh(model)
        
        # Map back to domain entity with Colombia timezone
        return Emotion(
            user_id=model.user_id,
            title=model.title,
            text=model.text,
            ai_response=model.ai_response,
            id=model.id,
            created_at=model.created_at_colombia
        )
    
    def find_all_by_user(self, user_id: UUID) -> list[Emotion]:
        """Find all emotions for a user, ordered by created_at desc."""
        stmt = select(EmotionModel).where(
            EmotionModel.user_id == user_id
        ).order_by(desc(EmotionModel.created_at))
        
        result = self.session.execute(stmt)
        models = result.scalars().all()
        
        return [
            Emotion(
                user_id=model.user_id,
                title=model.title,
                text=model.text,
                ai_response=model.ai_response,
                id=model.id,
                created_at=model.created_at_colombia
            )
            for model in models
        ]
    
    def has_emotion_on_date(self, user_id: UUID, check_date: date) -> bool:
        """Check if user has any emotion on given date (Colombia timezone)."""
        # Convert timestamp to Colombia timezone before extracting date
        stmt = select(func.count(EmotionModel.id)).where(
            and_(
                EmotionModel.user_id == user_id,
                func.date(func.timezone('America/Bogota', EmotionModel.created_at)) == check_date
            )
        )
        result = self.session.execute(stmt)
        count = result.scalar()
        return count > 0
    
    def get_emotion_dates_for_user(self, user_id: UUID) -> list[date]:
        """Get all unique dates when user created emotions (Colombia timezone), ordered desc."""
        # Convert timestamp to Colombia timezone before extracting date
        stmt = select(
            func.date(func.timezone('America/Bogota', EmotionModel.created_at)).label('emotion_date')
        ).where(
            EmotionModel.user_id == user_id
        ).group_by(
            func.date(func.timezone('America/Bogota', EmotionModel.created_at))
        ).order_by(
            desc('emotion_date')
        )
        
        result = self.session.execute(stmt)
        return [row[0] for row in result.fetchall()]
