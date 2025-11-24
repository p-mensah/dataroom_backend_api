from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    company: str
    phone: Optional[str] = None
    permission_level_id: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    company: str
    phone: Optional[str]
    permission_level_id: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    permission_level_id: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    """Response model for a user"""

    id: str
    name: str
    email: str
    role_id: str
    permission_level_id: int  # Add this line
    created_at: datetime
    updated_at: datetime