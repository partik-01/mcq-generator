"""
MCQ and learning session Pydantic schemas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class MCQBase(BaseModel):
    """Base MCQ schema"""
    question: str = Field(..., description="Question text")
    option_a: str = Field(..., max_length=500, description="Option A")
    option_b: str = Field(..., max_length=500, description="Option B")
    option_c: str = Field(..., max_length=500, description="Option C")
    option_d: str = Field(..., max_length=500, description="Option D")
    correct_answer: str = Field(..., pattern="^[ABCD]$", description="Correct answer")
    explanation: Optional[str] = Field(None, description="Answer explanation")


class MCQCreate(MCQBase):
    """Schema for creating MCQs"""
    topic_id: Optional[int] = None
    subtopic_id: Optional[int] = None
    difficulty_level: int = Field(1, ge=1, le=5, description="Difficulty level 1-5")
    ai_generated_metadata: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "topic_id": 1,
                "question": "What is the determinant of a 2x2 identity matrix?",
                "option_a": "0",
                "option_b": "1", 
                "option_c": "2",
                "option_d": "-1",
                "correct_answer": "B",
                "explanation": "The determinant of any identity matrix is 1",
                "difficulty_level": 2
            }
        }
    )


class MCQUpdate(BaseModel):
    """Schema for updating MCQs"""
    question: Optional[str] = None
    option_a: Optional[str] = Field(None, max_length=500)
    option_b: Optional[str] = Field(None, max_length=500)
    option_c: Optional[str] = Field(None, max_length=500)
    option_d: Optional[str] = Field(None, max_length=500)
    correct_answer: Optional[str] = Field(None, pattern="^[ABCD]$")
    explanation: Optional[str] = None
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    is_active: Optional[bool] = None


class MCQResponse(MCQBase):
    """Schema for MCQ response"""
    id: int
    topic_id: Optional[int] = None
    subtopic_id: Optional[int] = None
    difficulty_level: int
    question_hash: Optional[str] = None
    ai_generated_metadata: Optional[Dict[str, Any]] = None
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class MCQForSession(BaseModel):
    """Schema for MCQ in a learning session (without correct answer)"""
    id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty_level: int
    explanation: Optional[str] = None  # Only shown after answering
    
    model_config = ConfigDict(from_attributes=True)


class UserSessionBase(BaseModel):
    """Base user session schema"""
    session_name: Optional[str] = Field(None, max_length=200, description="Session name")
    questions_per_session: int = Field(10, ge=1, le=50, description="Questions per session")


class UserSessionCreate(UserSessionBase):
    """Schema for creating user sessions"""
    topic_ids: Optional[List[int]] = Field(None, description="Topic IDs for this session")
    target_difficulty: int = Field(1, ge=1, le=5, description="Target difficulty level")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_name": "Linear Algebra Practice",
                "topic_ids": [1, 2, 3],
                "target_difficulty": 2,
                "questions_per_session": 15
            }
        }
    )


class UserSessionResponse(UserSessionBase):
    """Schema for user session response"""
    id: int
    user_id: int
    topic_ids: Optional[List[int]] = None
    target_difficulty: int
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    last_activity: datetime
    
    # Session metrics
    total_questions: int
    correct_answers: int
    current_streak: int
    accuracy_percentage: Optional[float] = None
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)


class UserResponseSubmit(BaseModel):
    """Schema for submitting MCQ answers"""
    mcq_id: int = Field(..., description="MCQ ID")
    selected_answer: str = Field(..., pattern="^[ABCD]$", description="Selected answer")
    time_taken: Optional[int] = Field(None, ge=0, description="Time taken in seconds")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "mcq_id": 123,
                "selected_answer": "B",
                "time_taken": 45
            }
        }
    )


class UserResponseCreate(UserResponseSubmit):
    """Schema for creating user responses (internal)"""
    user_id: int
    session_id: int
    is_correct: bool
    question_difficulty_at_time: Optional[int] = None
    response_metadata: Optional[Dict[str, Any]] = None


class UserResponseResult(BaseModel):
    """Schema for user response result"""
    id: int
    mcq_id: int
    selected_answer: str
    correct_answer: str
    is_correct: bool
    time_taken: Optional[int] = None
    explanation: Optional[str] = None
    
    # Next question info
    next_mcq: Optional[MCQForSession] = None
    session_complete: bool = False
    
    model_config = ConfigDict(from_attributes=True)


class FlashcardBase(BaseModel):
    """Base flashcard schema"""
    front_content: str = Field(..., description="Front content (question/prompt)")
    back_content: str = Field(..., description="Back content (answer/explanation)")


class FlashcardCreate(FlashcardBase):
    """Schema for creating flashcards"""
    topic_id: Optional[int] = None
    subtopic_id: Optional[int] = None
    difficulty_level: int = Field(1, ge=1, le=5, description="Difficulty level 1-5")
    ai_generated_metadata: Optional[Dict[str, Any]] = None


class FlashcardResponse(FlashcardBase):
    """Schema for flashcard response"""
    id: int
    topic_id: Optional[int] = None
    subtopic_id: Optional[int] = None
    difficulty_level: int
    card_hash: Optional[str] = None
    ai_generated_metadata: Optional[Dict[str, Any]] = None
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class SessionSummary(BaseModel):
    """Schema for session performance summary"""
    session_id: int
    total_questions: int
    correct_answers: int
    accuracy_percentage: float
    current_streak: int
    average_time_per_question: Optional[float] = None
    difficulty_breakdown: Dict[int, Dict[str, int]] = {}  # {difficulty: {correct: X, total: Y}}
    topic_breakdown: Dict[int, Dict[str, int]] = {}      # {topic_id: {correct: X, total: Y}}