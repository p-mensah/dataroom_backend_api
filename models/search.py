from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DocumentSearchQuery(BaseModel):
    query: str = Field(..., min_length=1, description="Search query text")
    document_type: Optional[str] = None
    categories: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    tags: Optional[List[str]] = []

class SearchResult(BaseModel):
    id: str
    title: str
    file_type: str
    category: str
    upload_date: datetime
    preview_text: Optional[str] = None
    file_path: str
    relevance_score: float
    highlight: Optional[str] = None

class SearchHistoryItem(BaseModel):
    id: str
    user_id: str
    query: str
    timestamp: datetime
    results_count: int
