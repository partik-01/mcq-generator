"""
API v1 router
"""

from fastapi import APIRouter

from app.api.v1 import auth

# Create API v1 router
api_router = APIRouter()

# Include route modules
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Future routers will be added here:
# api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
# api_router.include_router(topics.router, prefix="/topics", tags=["topics"])  
# api_router.include_router(mcqs.router, prefix="/mcqs", tags=["mcqs"])