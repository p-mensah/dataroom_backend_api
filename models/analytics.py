from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

class ActivityStats(BaseModel):
    active_users: int
    total_views: int
    total_downloads: int
    average_time_spent: float

class DocumentHeatmap(BaseModel):
    document_id: str
    document_title: str
    view_count: int
    download_count: int

class InvestorActivity(BaseModel):
    investor_id: str
    investor_name: str
    last_active: datetime
    documents_viewed: int
    time_spent_minutes: int