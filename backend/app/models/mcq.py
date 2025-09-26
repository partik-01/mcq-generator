"""
MCQ and related models for adaptive learning system
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, CHAR, JSON, text, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class MCQ(Base):
    """Multiple Choice Question model"""
    __tablename__ = "mcqs"
    
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    subtopic_id = Column(Integer, ForeignKey("subtopics.id"), nullable=True)
    
    # Question content
    question = Column(Text, nullable=False)
    option_a = Column(String(500), nullable=False)
    option_b = Column(String(500), nullable=False) 
    option_c = Column(String(500), nullable=False)
    option_d = Column(String(500), nullable=False)
    correct_answer = Column(CHAR(1), nullable=False)
    explanation = Column(Text, nullable=True)
    
    # Question metadata
    difficulty_level = Column(Integer, default=1, nullable=False)
    question_hash = Column(String(64), unique=True, nullable=True)  # Duplicate prevention
    ai_generated_metadata = Column(JSON, nullable=True)  # AI generation parameters
    
    # Status
    is_active = Column(Boolean, default=True, server_default=text('TRUE'))
    created_at = Column(DateTime, default=datetime.utcnow, server_default=text('CURRENT_TIMESTAMP'))
    
    # Constraints
    __table_args__ = (
        CheckConstraint("correct_answer IN ('A', 'B', 'C', 'D')", name='valid_correct_answer'),
        CheckConstraint("difficulty_level BETWEEN 1 AND 5", name='valid_difficulty_level'),
    )
    
    # Relationships
    topic = relationship("Topic", back_populates="mcqs")
    subtopic = relationship("Subtopic", back_populates="mcqs")
    user_responses = relationship("UserResponse", back_populates="mcq")
    
    def __repr__(self):
        return f"<MCQ(id={self.id}, difficulty={self.difficulty_level}, correct={self.correct_answer})>"
    
    @property
    def options_dict(self) -> Dict[str, str]:
        """Returns options as a dictionary"""
        return {
            'A': self.option_a,
            'B': self.option_b,
            'C': self.option_c,
            'D': self.option_d
        }
    
    def is_correct_answer(self, answer: str) -> bool:
        """Check if provided answer is correct"""
        return answer.upper() == self.correct_answer


class UserSession(Base):
    """User learning session model"""
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Session metadata
    session_name = Column(String(200), nullable=True)
    topic_ids = Column(JSON, nullable=True)  # List of topic IDs for this session
    target_difficulty = Column(Integer, default=1, nullable=False)
    questions_per_session = Column(Integer, default=10, nullable=False)
    
    # Session status
    status = Column(String(20), default="active", server_default=text("'active'"))
    # Status options: active, paused, completed, abandoned
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow, server_default=text('CURRENT_TIMESTAMP'))
    completed_at = Column(DateTime, nullable=True)
    last_activity = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Session metrics
    total_questions = Column(Integer, default=0, server_default=text('0'))
    correct_answers = Column(Integer, default=0, server_default=text('0'))
    current_streak = Column(Integer, default=0, server_default=text('0'))
    
    # Relationships
    user = relationship("User", back_populates="user_sessions")
    user_responses = relationship("UserResponse", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id}, status='{self.status}')>"
    
    @property
    def accuracy_percentage(self) -> Optional[float]:
        """Calculate accuracy percentage"""
        if self.total_questions > 0:
            return round((self.correct_answers / self.total_questions) * 100, 1)
        return None
    
    @property
    def is_active(self) -> bool:
        """Check if session is active"""
        return self.status == "active"


class UserResponse(Base):
    """User response to MCQ model"""
    __tablename__ = "user_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(Integer, ForeignKey("user_sessions.id", ondelete="CASCADE"), nullable=False)
    mcq_id = Column(Integer, ForeignKey("mcqs.id"), nullable=False)
    
    # Response data
    selected_answer = Column(CHAR(1), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_taken = Column(Integer, nullable=True)  # Time in seconds
    
    # Context
    question_difficulty_at_time = Column(Integer, nullable=True)  # Difficulty when question was asked
    response_metadata = Column(JSON, nullable=True)  # Additional response context
    
    # Timestamps
    answered_at = Column(DateTime, default=datetime.utcnow, server_default=text('CURRENT_TIMESTAMP'))
    
    # Constraints
    __table_args__ = (
        CheckConstraint("selected_answer IN ('A', 'B', 'C', 'D')", name='valid_selected_answer'),
    )
    
    # Relationships
    user = relationship("User", back_populates="user_responses")
    session = relationship("UserSession", back_populates="user_responses")
    mcq = relationship("MCQ", back_populates="user_responses")
    
    def __repr__(self):
        return f"<UserResponse(id={self.id}, answer='{self.selected_answer}', correct={self.is_correct})>"


class Flashcard(Base):
    """Flashcard model for spaced repetition learning"""
    __tablename__ = "flashcards"
    
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    subtopic_id = Column(Integer, ForeignKey("subtopics.id"), nullable=True)
    
    # Flashcard content
    front_content = Column(Text, nullable=False)  # Question/prompt
    back_content = Column(Text, nullable=False)   # Answer/explanation
    
    # Metadata
    difficulty_level = Column(Integer, default=1, nullable=False)
    card_hash = Column(String(64), unique=True, nullable=True)  # Duplicate prevention
    ai_generated_metadata = Column(JSON, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, server_default=text('TRUE'))
    created_at = Column(DateTime, default=datetime.utcnow, server_default=text('CURRENT_TIMESTAMP'))
    
    # Constraints
    __table_args__ = (
        CheckConstraint("difficulty_level BETWEEN 1 AND 5", name='flashcard_valid_difficulty'),
    )
    
    # Relationships
    topic = relationship("Topic", back_populates="flashcards")
    subtopic = relationship("Subtopic", back_populates="flashcards")
    flashcard_reviews = relationship("FlashcardReview", back_populates="flashcard")
    
    def __repr__(self):
        return f"<Flashcard(id={self.id}, difficulty={self.difficulty_level})>"


class FlashcardReview(Base):
    """Flashcard review tracking for spaced repetition"""
    __tablename__ = "flashcard_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    flashcard_id = Column(Integer, ForeignKey("flashcards.id", ondelete="CASCADE"), nullable=False)
    
    # Review data
    ease_factor = Column(Integer, nullable=False)  # 1-5 scale (1=again, 5=easy)
    review_interval = Column(Integer, default=1, nullable=False)  # Days until next review
    next_review_date = Column(DateTime, nullable=False)
    
    # Timestamps
    reviewed_at = Column(DateTime, default=datetime.utcnow, server_default=text('CURRENT_TIMESTAMP'))
    
    # Constraints
    __table_args__ = (
        CheckConstraint("ease_factor BETWEEN 1 AND 5", name='valid_ease_factor'),
    )
    
    # Relationships
    user = relationship("User")
    flashcard = relationship("Flashcard", back_populates="flashcard_reviews")
    
    def __repr__(self):
        return f"<FlashcardReview(id={self.id}, ease={self.ease_factor}, interval={self.review_interval})>"