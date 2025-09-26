"""
Authentication-related Pydantic schemas
"""

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """JWT Token response schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # Seconds until expiration


class TokenData(BaseModel):
    """Token payload data schema"""
    user_id: Optional[int] = None
    username: Optional[str] = None


class PasswordReset(BaseModel):
    """Password reset request schema"""
    email: str


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema"""
    token: str
    new_password: str