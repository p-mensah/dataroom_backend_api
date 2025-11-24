from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class DocumentCategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    parent_category_id: Optional[str] = None
    sort_order: int = 0


class DocumentCategoryResponse(BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str]
    parent_category_id: Optional[str]
    sort_order: int
    is_active: bool
    created_at: datetime


class DocumentUpload(BaseModel):
    title: str
    description: Optional[str] = None
    category_id: str


class DocumentResponse(BaseModel):
    id: str
    category_id: str
    title: str
    description: Optional[str]
    file_name: str
    file_type: str
    file_size: int
    version_number: int
    is_latest_version: bool
    uploaded_by: str
    uploaded_at: datetime
    updated_at: datetime


class DocumentAccessLog(BaseModel):
    document_id: str
    user_id: str
    action: str
    ip_address: str
    user_agent: str
