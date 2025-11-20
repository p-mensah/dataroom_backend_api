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
    full_name: str
    company: str
    phone: Optional[str]
    message: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

class AccessRequestUpdate(BaseModel):
    status: str
    admin_notes: Optional[str] = None
    expires_at: Optional[datetime] = None