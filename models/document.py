# # models/document.py
# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional, List

# class DocumentCategoryCreate(BaseModel):
#     name: str
#     description: Optional[str] = None

# class DocumentCategoryResponse(DocumentCategoryCreate):  # This is the missing one for the import
#     id: str

# class DocumentCreate(BaseModel):
#     title: str
#     description: Optional[str] = None
#     category: str
#     tags: List[str] = []

# class DocumentResponse(BaseModel):
#     id: str
#     title: str
#     description: Optional[str]
#     file_path: str
#     file_type: str
#     category: str
#     file_size: int
#     uploaded_at: datetime
#     tags: List[str]
#     view_count: int
#     download_count: int

# class DocumentUpload(BaseModel):  # Also needed by import chain
#     name: str
#     category_id: str
#     file_path: str
#     uploaded_at: Optional[datetime] = None

# class DocumentSearch(BaseModel):
#     query: Optional[str] = None
#     category: Optional[str] = None
#     date_from: Optional[datetime] = None
#     date_to: Optional[datetime] = None
#     tags: Optional[List[str]] = None

# class DocumentAccessLog(BaseModel): # If imported elsewhere
#     document_id: str
#     user_id: str
#     action: str  # e.g., "view", "download"
#     timestamp: datetime = datetime.utcnow()






from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class DocumentCategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class DocumentCategoryResponse(DocumentCategoryCreate):  # This was added earlier
    id: str

class DocumentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    tags: List[str] = []

class DocumentResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    file_path: str
    file_type: str
    category: str
    file_size: int
    uploaded_at: datetime
    tags: List[str]
    view_count: int
    download_count: int

class DocumentUpload(BaseModel):  # This was added earlier
    name: str
    category_id: str
    file_path: str
    uploaded_at: Optional[datetime] = None

class DocumentAccessLog(BaseModel):  # Add this class
    document_id: str
    user_id: str
    action: str  # e.g., "view", "download"
    timestamp: datetime = datetime.utcnow()

class DocumentSearch(BaseModel):
    query: Optional[str] = None
    category: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    tags: Optional[List[str]] = None