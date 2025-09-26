"""
Authentication service for user management
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.schemas.auth import Token
from app.core.security import create_access_token, verify_password, get_password_hash


class AuthService:
    def __init__(self):
        pass
    
    async def register_user(self, db: AsyncSession, user_data: UserCreate) -> User:
        """Register a new user"""
        
        # Check if username already exists
        result = await db.execute(select(User).filter(User.username == user_data.username))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        result = await db.execute(select(User).filter(User.email == user_data.email))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        return db_user
    
    async def authenticate_user(self, db: AsyncSession, login_data: UserLogin) -> Optional[User]:
        """Authenticate user login"""
        
        # Try to find user by username or email
        result = await db.execute(
            select(User).filter(
                (User.username == login_data.username) | 
                (User.email == login_data.username)
            )
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        if not verify_password(login_data.password, user.password_hash):
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        await db.commit()
        
        return user
    
    async def create_access_token_for_user(self, user: User) -> Token:
        """Create JWT access token for user"""
        
        access_token = create_access_token(subject=str(user.id))
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=3600  # 1 hour
        )
    
    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        """Get user by username"""
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none()


# Global auth service instance
auth_service = AuthService()