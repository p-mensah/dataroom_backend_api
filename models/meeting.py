from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MeetingCreate(BaseModel):
    scheduled_at: datetime
    duration_minutes: int = 30
    notes: Optional[str] = None

class MeetingResponse(BaseModel):
    id: str
    investor_id: str
    scheduled_at: datetime
    duration_minutes: int
    meeting_link: str
    status: str
    created_at: datetime