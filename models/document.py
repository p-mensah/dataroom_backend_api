from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

# Define the fixed document categories
class DocumentCategory(str, Enum):
    COMPANY_OVERVIEW = "Company Overview"
    MARKET_IMPACT = "Market & Impact"
    FINANCIALS = "Financials"
    IP_TECHNOLOGY = "IP & Technology"
    TRACTION = "Traction"
    LEGAL = "Legal"
    OTHERS = "Others"

class DocumentCategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class DocumentCategoryResponse(DocumentCategoryCreate):
    id: str

class DocumentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    categories: List[str]  
    tags: List[str] = []
    
    @field_validator('categories')
    @classmethod
    def validate_categories(cls, v):
        if not v or len(v) == 0:
            raise ValueError('At least one category must be selected')
        if len(v) > 3:
            raise ValueError('Maximum 3 categories allowed')
        
        # Validate each category against allowed values
        valid_categories = [cat.value for cat in DocumentCategory]
        for category in v:
            if category not in valid_categories:
                raise ValueError(f'Invalid category: {category}. Must be one of: {", ".join(valid_categories)}')
        
        # Remove duplicates
        return list(set(v))

class DocumentResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    file_path: str
    file_url: str  
    file_type: str
    categories: List[str]  
    file_size: int
    uploaded_at: datetime
    uploaded_by: str  
    tags: List[str]
    view_count: int = 0
    download_count: int = 0

class DocumentUpload(BaseModel):
    name: str
    categories: List[str]  
    file_path: str
    uploaded_at: Optional[datetime] = None
    
    @field_validator('categories')
    @classmethod
    def validate_categories(cls, v):
        if not v or len(v) == 0:
            raise ValueError('At least one category must be selected')
        if len(v) > 3:
            raise ValueError('Maximum 3 categories allowed')
        return list(set(v))

class DocumentAccessLog(BaseModel):
    document_id: str
    user_id: str
    action: str  
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    ip_address: Optional[str] = None  
    user_agent: Optional[str] = None  

class DocumentSearch(BaseModel):
    query: Optional[str] = None
    categories: Optional[List[str]] = None  
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    tags: Optional[List[str]] = None
    
    @field_validator('categories')
    @classmethod
    def validate_categories(cls, v):
        if v is None:
            return v
        
        valid_categories = [cat.value for cat in DocumentCategory]
        for category in v:
            if category not in valid_categories:
                raise ValueError(f'Invalid category: {category}')
        return v

# Helper class for category list endpoint
class CategoryListResponse(BaseModel):
    categories: List[dict] = [
        {"value": "Company Overview", "label": "Company Overview"},
        {"value": "Market & Impact", "label": "Market & Impact"},
        {"value": "Financials", "label": "Financials"},
        {"value": "IP & Technology", "label": "IP & Technology"},
        {"value": "Traction", "label": "Traction"},
        {"value": "Legal", "label": "Legal"},
        {"value": "Others", "label": "Others"}
    ]

# Stats response model
class DocumentStatsResponse(BaseModel):
    total_documents: int
    by_category: List[dict]
    total_views: int = 0
    total_downloads: int = 0