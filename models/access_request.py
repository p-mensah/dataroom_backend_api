from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class AccessRequestCreate(BaseModel):
    """
    Represents the data required to create a new access request.
    """
    email: EmailStr
    full_name: str
    company: str
    phone: Optional[str] = None
    message: Optional[str] = None

class AccessRequestResponse(BaseModel):
    """
    Represents the data returned for an access request.
    """
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
    """
    Represents the data required to update an access request.
    """
    status: str
    admin_notes: Optional[str] = None
    expires_at: Optional[datetime] = None