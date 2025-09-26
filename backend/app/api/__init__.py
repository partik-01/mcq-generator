"""
Main API router
"""

from fastapi import APIRouter

from app.api.v1 import api_router as v1_router

# Create main API router
router = APIRouter()

# Include API versions
router.include_router(v1_router, prefix="/v1")