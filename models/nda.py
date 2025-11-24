from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NDAAcceptance(BaseModel):
    digital_signature: str
    ip_address: str
    user_agent: str


class NDAResponse(BaseModel):
    id: str
    user_id: str
    nda_version: str
    digital_signature: str
    ip_address: str
    accepted_at: datetime
    is_active: bool


class NDAContent(BaseModel):
    version: str
    content: str
    effective_date: datetime
