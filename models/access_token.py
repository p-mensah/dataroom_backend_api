from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AccessTokenCreate(BaseModel):
    """
    Represents the data required to create a new access token.
    """
    access_request_id: str
    email: str
    expires_at: Optional[datetime] = None

class AccessTokenResponse(BaseModel):
    """
    Represents the data returned for an access token.
    """
    id: str
    token: str
    email: str
    expires_at: Optional[datetime]
    is_active: bool
    created_at: datetime