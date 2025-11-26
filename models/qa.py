from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class QAThreadCreate(BaseModel):
    question: str
    category: str
    is_public: bool = False

class QAResponseCreate(BaseModel):
    response_text: str

class QAThreadResponse(BaseModel):
    id: str
    investor_id: str
    question: str
    category: str
    status: str
    created_at: datetime
    is_public: bool
    responses: list = []