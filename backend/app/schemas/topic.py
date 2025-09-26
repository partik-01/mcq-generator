"""
Topic and Subtopic Pydantic schemas
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal


class TopicBase(BaseModel):
    """Base topic schema"""
    title: str = Field(..., max_length=200, description="Topic title")
    description: Optional[str] = Field(None, description="Topic description")


class TopicCreate(TopicBase):
    """Schema for creating topics"""
    document_id: int = Field(..., description="Document ID")
    extracted_content: Optional[str] = None
    topic_order: Optional[int] = None
    ai_confidence_score: Optional[Decimal] = Field(None, ge=0, le=1)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "document_id": 1,
                "title": "Linear Algebra Fundamentals",
                "description": "Basic concepts of linear algebra including vectors and matrices",
                "topic_order": 1,
                "ai_confidence_score": 0.95
            }
        }
    )


class TopicUpdate(BaseModel):
    """Schema for updating topics"""
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    extracted_content: Optional[str] = None
    topic_order: Optional[int] = None
    ai_confidence_score: Optional[Decimal] = Field(None, ge=0, le=1)


class SubtopicBase(BaseModel):
    """Base subtopic schema"""
    title: str = Field(..., max_length=200, description="Subtopic title")
    description: Optional[str] = Field(None, description="Subtopic description")


class SubtopicCreate(SubtopicBase):
    """Schema for creating subtopics"""
    topic_id: int = Field(..., description="Parent topic ID")
    extracted_content: Optional[str] = None
    subtopic_order: Optional[int] = None
    ai_confidence_score: Optional[Decimal] = Field(None, ge=0, le=1)


class SubtopicResponse(SubtopicBase):
    """Schema for subtopic response"""
    id: int
    topic_id: int
    extracted_content: Optional[str] = None
    subtopic_order: Optional[int] = None
    ai_confidence_score: Optional[Decimal] = None
    confidence_percentage: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    # Related counts
    mcqs_count: int = 0
    flashcards_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)


class TopicResponse(TopicBase):
    """Schema for topic response"""
    id: int
    document_id: int
    extracted_content: Optional[str] = None
    topic_order: Optional[int] = None
    ai_confidence_score: Optional[Decimal] = None
    confidence_percentage: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    # Related data
    subtopics: List[SubtopicResponse] = []
    
    # Related counts
    subtopics_count: int = 0
    mcqs_count: int = 0
    flashcards_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)


class TopicList(BaseModel):
    """Schema for topic list with pagination"""
    topics: List[TopicResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class TopicSummary(BaseModel):
    """Schema for topic summary (without content)"""
    id: int
    title: str
    description: Optional[str] = None
    topic_order: Optional[int] = None
    confidence_percentage: Optional[int] = None
    subtopics_count: int = 0
    mcqs_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)