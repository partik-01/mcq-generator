"""
AI MCQ Generator FastAPI Application

This is the main FastAPI application module that initializes the app,
configures middleware, and sets up routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import close_db, init_db

# Create FastAPI application instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent MCQ and flashcard generation system using AI",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    debug=settings.DEBUG
)

# Configure CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    
    This function runs when the FastAPI application starts up.
    It initializes the database and performs any necessary setup.
    """
    print(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"📊 Environment: {settings.ENVIRONMENT}")
    print(f"🔗 API Documentation: http://{settings.SERVER_HOST}:{settings.SERVER_PORT}{settings.API_V1_STR}/docs")
    
    # Initialize database
    try:
        await init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event handler.
    
    This function runs when the FastAPI application shuts down.
    It performs cleanup operations like closing database connections.
    """
    print("🛑 Shutting down AI MCQ Generator...")
    
    # Close database connections
    try:
        await close_db()
        print("✅ Database connections closed")
    except Exception as e:
        print(f"❌ Error closing database connections: {e}")


@app.get("/")
async def root():
    """
    Root endpoint for health check.
    
    Returns:
        dict: Basic application information
    """
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "status": "healthy",
        "docs_url": f"{settings.API_V1_STR}/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Application health status
    """
    return {
        "status": "healthy",
        "timestamp": "2025-09-26",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


# Include API routes (will be added in Phase 2)
# from app.api.v1.api import api_router
# app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )