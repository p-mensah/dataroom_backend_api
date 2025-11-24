from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PermissionLevelCreate(BaseModel):
    name: str
    description: str
    can_view: bool = True
    can_download: bool = False
    has_expiry: bool = False
    max_downloads: Optional[int] = None

class PermissionLevelResponse(BaseModel):
    id: str
    name: str
    description: str
    can_view: bool
    can_download: bool
    has_expiry: bool
    max_downloads: Optional[int]
    created_at: datetime

class PermissionLevelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    can_view: Optional[bool] = None
    can_download: Optional[bool] = None
    has_expiry: Optional[bool] = None
    max_downloads: Optional[int] = None