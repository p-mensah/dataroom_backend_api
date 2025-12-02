from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class QuestionCreate(BaseModel):
    question_text: str = Field(..., min_length=10)
    category: str
    is_urgent: bool = False

class AnswerCreate(BaseModel):
    answer_text: str = Field(..., min_length=5)
    is_public: bool = False

class QAThreadResponse(BaseModel):
    id: str
    question_text: str
    category: str
    asked_by: str
    asked_at: datetime
    answer_text: Optional[str] = None
    answered_by: Optional[str] = None
    answered_at: Optional[datetime] = None
    is_public: bool
    is_urgent: bool
    status: str  # "pending", "answered", "archived"