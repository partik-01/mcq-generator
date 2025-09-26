"""
Pydantic schemas for API request/response models
"""

from .user import UserCreate, UserUpdate, UserResponse, UserLogin  # noqa
from .document import DocumentCreate, DocumentResponse, DocumentUpdate  # noqa
from .topic import TopicCreate, TopicResponse, TopicUpdate, SubtopicCreate, SubtopicResponse  # noqa
from .mcq import (  # noqa
    MCQCreate, MCQResponse, MCQUpdate,
    UserSessionCreate, UserSessionResponse, 
    UserResponseCreate, UserResponseSubmit,
    FlashcardCreate, FlashcardResponse
)
from .auth import Token, TokenData  # noqa

__all__ = [
    # User schemas
    "UserCreate", "UserUpdate", "UserResponse", "UserLogin",
    # Document schemas  
    "DocumentCreate", "DocumentResponse", "DocumentUpdate",
    # Topic schemas
    "TopicCreate", "TopicResponse", "TopicUpdate", 
    "SubtopicCreate", "SubtopicResponse",
    # MCQ schemas
    "MCQCreate", "MCQResponse", "MCQUpdate",
    "UserSessionCreate", "UserSessionResponse",
    "UserResponseCreate", "UserResponseSubmit",
    "FlashcardCreate", "FlashcardResponse",
    # Auth schemas
    "Token", "TokenData"
]