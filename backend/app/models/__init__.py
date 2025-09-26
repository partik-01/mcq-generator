"""
Database models package initialization
"""

# Import all models here to ensure they are registered with SQLAlchemy
# This is important for Alembic migrations to work properly

from .user import User  # noqa
from .document import Document  # noqa  
from .topic import Topic, Subtopic  # noqa
from .mcq import MCQ, UserSession, UserResponse, Flashcard, FlashcardReview  # noqa

# Export all models for easy importing
__all__ = [
    "User",
    "Document", 
    "Topic",
    "Subtopic",
    "MCQ",
    "UserSession", 
    "UserResponse",
    "Flashcard",
    "FlashcardReview"
]