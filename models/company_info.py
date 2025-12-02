from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class KeyMetric(BaseModel):
    metric_name: str
    value: str
    trend: Optional[str] = None  # "up", "down", "stable"
    last_updated: datetime

class Milestone(BaseModel):
    date: datetime
    title: str
    description: str
    category: str  # "funding", "product", "growth", "partnership"

class Testimonial(BaseModel):
    id: str
    customer_name: str
    company: str
    position: str
    testimonial_text: str
    rating: Optional[int] = None
    date_added: datetime
    is_featured: bool = False

class Award(BaseModel):
    id: str
    award_name: str
    awarding_body: str
    date_received: datetime
    logo_url: Optional[str] = None
    description: Optional[str] = None

class MediaCoverage(BaseModel):
    id: str
    publication_name: str
    article_title: str
    article_url: str
    publish_date: datetime
    logo_url: Optional[str] = None