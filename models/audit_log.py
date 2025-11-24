from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AuditLogCreate(BaseModel):
    access_request_id: str
    admin_id: Optional[str] = None
    action: str
    previous_status: Optional[str] = None
    new_status: Optional[str] = None
    notes: Optional[str] = None


class AuditLogResponse(BaseModel):
    id: str
    access_request_id: str
    admin_id: Optional[str]
    action: str
    previous_status: Optional[str]
    new_status: Optional[str]
    notes: Optional[str]
    timestamp: datetime


class AuditLogFilter(BaseModel):
    access_request_id: Optional[str] = None
    admin_id: Optional[str] = None
    action: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
