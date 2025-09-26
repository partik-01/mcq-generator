"""
Database configuration and session management for AI MCQ Generator

This module sets up the async PostgreSQL database connection using SQLAlchemy 2.0+
with connection pooling optimized for AI workloads.
"""

import os
from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create async engine with optimized configuration for AI workloads
async_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,     # Handle concurrent AI requests
    max_overflow=settings.DATABASE_MAX_OVERFLOW,  # Prevent connection exhaustion
    pool_pre_ping=True,                        # Handle connection drops gracefully
    echo=settings.DEBUG,                       # Log SQL in development
    future=True                                # Use SQLAlchemy 2.0 style
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Naming convention for constraints (helps with migrations)
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)

# Base class for all database models
Base = declarative_base(metadata=metadata)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to get database session for FastAPI endpoints.
    
    This function provides an async database session with proper
    transaction handling and cleanup.
    
    Yields:
        AsyncSession: Database session for the request
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initialize database tables.
    
    This function creates all tables defined in the models.
    Should be called during application startup.
    """
    async with async_engine.begin() as conn:
        # Import all models here to ensure they are registered
        from app.models import user, document, topic, mcq  # noqa
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """
    Close database connections.
    
    This function should be called during application shutdown
    to properly close all database connections.
    """
    await async_engine.dispose()