from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class InvestorCreate(BaseModel):
    email: EmailStr
    full_name: str
    company: str
    access_token_id: str
    is_high_value: bool = False

class InvestorResponse(BaseModel):
    id: str
    email: str
    full_name: str
    company: str
    is_high_value: bool
    created_at: datetime
