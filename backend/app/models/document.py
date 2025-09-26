"""
Document model for PDF and file management
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Document(Base):
    """Document model for PDF and file management"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # File information
    filename = Column(String(255), nullable=False)  # Stored filename
    original_filename = Column(String(255), nullable=False)  # Original upload filename
    file_path = Column(String(500), nullable=False)  # Path to stored file
    file_size = Column(Integer, nullable=True)  # File size in bytes
    mime_type = Column(String(50), nullable=True)  # MIME type
    document_hash = Column(String(64), unique=True, nullable=True)  # SHA-256 hash for duplicate detection
    
    # Processing status
    processing_status = Column(String(20), default="pending", server_default=text("'pending'"))
    # Status options: pending, processing, completed, failed
    
    # Timestamps
    upload_date = Column(DateTime, default=datetime.utcnow, server_default=text('CURRENT_TIMESTAMP'))
    extraction_completed_at = Column(DateTime, nullable=True)
    
    # Metadata (JSON field for flexible document metadata)
    document_metadata = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="documents")
    topics = relationship("Topic", back_populates="document", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}', status='{self.processing_status}')>"
    
    @property
    def is_processed(self) -> bool:
        """Check if document processing is completed"""
        return self.processing_status == "completed"
    
    @property
    def file_size_mb(self) -> Optional[float]:
        """Returns file size in MB if available"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return None