from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AccessTokenCreate(BaseModel):
    access_request_id: str
    email: str
    expires_at: Optional[datetime] = None


class AccessTokenResponse(BaseModel):
    id: str
    token: str
    email: str
    expires_at: Optional[datetime]
    is_active: bool
    created_at: datetime
