from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class AccessRequestCreate(BaseModel):
    email: EmailStr
    full_name: str
    company: str
    phone: Optional[str] = None
    message: Optional[str] = None

class AccessRequestResponse(BaseModel):
    id: str
    email: str
    full_name: str  # Not 'name'
    company: str
    phone: Optional[str] = None
    message: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    admin_notes: Optional[str] = None
    
    # Optional OTP fields
    otp_verified: Optional[bool] = None
    email_verified: Optional[bool] = None
    verified_at: Optional[datetime] = None

class AccessRequestUpdate(BaseModel):
    status: str
    admin_notes: Optional[str] = None
    expires_at: Optional[datetime] = None