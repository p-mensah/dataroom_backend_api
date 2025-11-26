# models/alert.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AlertConfigCreate(BaseModel):
    user_id: str
    alert_type: str  # e.g., "document_update", "meeting_reminder", "access_expiration"
    is_active: bool = True

class AlertConfigUpdate(BaseModel):
    is_active: Optional[bool] = None
    alert_type: Optional[str] = None

class AlertConfigResponse(AlertConfigCreate):
    id: str
    created_at: datetime
    updated_at: datetime

class AlertLogCreate(BaseModel):
    alert_config_id: str
    message: str
    status: str = "pending"  # pending, sent, failed

class AlertLogResponse(AlertLogCreate):
    id: str
    sent_at: datetime