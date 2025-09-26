"""
Topic and Subtopic models for content organization
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric, text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Topic(Base):
    """Topic model for organizing document content"""
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    
    # Content
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    extracted_content = Column(Text, nullable=True)  # Content extracted from PDF
    
    # Organization
    topic_order = Column(Integer, nullable=True)  # Order within document
    ai_confidence_score = Column(Numeric(3, 2), nullable=True)  # AI confidence 0.00-1.00
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    document = relationship("Document", back_populates="topics")
    subtopics = relationship("Subtopic", back_populates="topic", cascade="all, delete-orphan")
    mcqs = relationship("MCQ", back_populates="topic")
    flashcards = relationship("Flashcard", back_populates="topic")
    
    def __repr__(self):
        return f"<Topic(id={self.id}, title='{self.title}', confidence={self.ai_confidence_score})>"
    
    @property
    def confidence_percentage(self) -> Optional[int]:
        """Returns confidence score as percentage"""
        if self.ai_confidence_score is not None:
            return int(float(self.ai_confidence_score) * 100)
        return None


class Subtopic(Base):
    """Subtopic model for detailed content organization"""
    __tablename__ = "subtopics"
    
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    
    # Content
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    extracted_content = Column(Text, nullable=True)
    
    # Organization
    subtopic_order = Column(Integer, nullable=True)  # Order within topic
    ai_confidence_score = Column(Numeric(3, 2), nullable=True)  # AI confidence 0.00-1.00
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    topic = relationship("Topic", back_populates="subtopics")
    mcqs = relationship("MCQ", back_populates="subtopic")
    flashcards = relationship("Flashcard", back_populates="subtopic")
    
    def __repr__(self):
        return f"<Subtopic(id={self.id}, title='{self.title}', topic_id={self.topic_id})>"
    
    @property
    def confidence_percentage(self) -> Optional[int]:
        """Returns confidence score as percentage"""
        if self.ai_confidence_score is not None:
            return int(float(self.ai_confidence_score) * 100)
        return None