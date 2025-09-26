"""
Document-related Pydantic schemas
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class DocumentBase(BaseModel):
    """Base document schema"""
    filename: str = Field(..., description="Document filename")
    original_filename: str = Field(..., description="Original upload filename")


class DocumentCreate(BaseModel):
    """Schema for document upload metadata"""
    original_filename: str = Field(..., description="Original filename")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "original_filename": "machine_learning_notes.pdf"
            }
        }
    )


class DocumentUpdate(BaseModel):
    """Schema for updating document metadata"""
    filename: Optional[str] = None
    processing_status: Optional[str] = Field(None, pattern="^(pending|processing|completed|failed)$")
    document_metadata: Optional[Dict[str, Any]] = None


class DocumentResponse(BaseModel):
    """Schema for document response"""
    id: int
    user_id: int
    filename: str
    original_filename: str
    file_path: str
    file_size: Optional[int] = None
    file_size_mb: Optional[float] = None
    mime_type: Optional[str] = None
    document_hash: Optional[str] = None
    processing_status: str
    upload_date: datetime
    extraction_completed_at: Optional[datetime] = None
    document_metadata: Optional[Dict[str, Any]] = None
    is_processed: bool
    
    # Related counts
    topics_count: int = 0
    mcqs_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)


class DocumentList(BaseModel):
    """Schema for paginated document list"""
    documents: list[DocumentResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class DocumentUploadResponse(BaseModel):
    """Schema for successful document upload"""
    document_id: int
    filename: str
    message: str
    processing_status: str