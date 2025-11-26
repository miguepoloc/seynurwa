"""Emotion domain exceptions."""


class EmotionError(Exception):
    """Base exception for emotion errors."""
    pass


class EmotionAlreadyExistsToday(EmotionError):
    """User already recorded an emotion today."""
    
    def __init__(self, user_id: str, date: str):
        self.user_id = user_id
        self.date = date
        super().__init__(f"User {user_id} already has an emotion for {date}")


class EmotionNotFound(EmotionError):
    """Emotion not found."""
    
    def __init__(self, user_id: str, date: str):
        self.user_id = user_id
        self.date = date
        super().__init__(f"No emotion found for user {user_id} on {date}")
