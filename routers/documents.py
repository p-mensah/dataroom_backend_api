from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from typing import List, Optional
from models.document import (
    DocumentCategoryCreate,
    DocumentCategoryResponse,
    DocumentUpload,
    DocumentResponse
)
from services.document_service import DocumentService
from services.permission_service import PermissionService
from services.nda_service import NDAService
from services.auth_service import AuthService
from database import (
    document_categories_collection,
    documents_collection,
    document_access_logs_collection
)
from bson import ObjectId
from datetime import datetime
import os

router = APIRouter(prefix="/api/documents", tags=["Documents"])
security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extract user ID from JWT token"""
    token = credentials.credentials
    payload = AuthService.verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload["sub"]

def check_nda_acceptance(user_id: str):
    """Middleware to check NDA acceptance"""
    if not NDAService.has_accepted_nda(user_id):
        raise HTTPException(
            status_code=403, 
            detail="NDA must be accepted before accessing documents"
        )

def check_access_validity(user_id: str):
    """Check if user's access is still valid"""
    if not PermissionService.check_access_expiry(user_id):
        raise HTTPException(
            status_code=403,
            detail="Access has expired"
        )


@router.get("/categories", response_model=List[DocumentCategoryResponse])
def list_categories(
    parent_id: Optional[str] = None,
    user_id: str = Depends(get_current_user_id)
):
    """List all document categories"""
    check_nda_acceptance(user_id)
    check_access_validity(user_id)
    
    query = {"is_active": True}
    if parent_id:
        query["parent_category_id"] = parent_id
    else:
        query["parent_category_id"] = None
    
    categories = list(document_categories_collection.find(query).sort("sort_order", 1))
    
    for cat in categories:
        cat["id"] = str(cat.pop("_id"))
    
    return categories

@router.get("/categories/{category_id}", response_model=DocumentCategoryResponse)
def get_category(
    category_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get specific category"""
    check_nda_acceptance(user_id)
    
    category = document_categories_collection.find_one({"_id": ObjectId(category_id)})
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category["id"] = str(category.pop("_id"))
    return category

@router.post("/categories", response_model=dict)
def create_category(category: DocumentCategoryCreate):
    """Create new document category (Admin only)"""
    existing = document_categories_collection.find_one({"slug": category.slug})
    if existing:
        raise HTTPException(status_code=400, detail="Category with this slug already exists")
    
    category_data = {
        **category.model_dump(),
        "is_active": True,
        "created_at": datetime.utcnow()
    }
    
    result = document_categories_collection.insert_one(category_data)
    
    return {
        "message": "Category created successfully",
        "id": str(result.inserted_id)
    }

@router.get("/categories/{category_id}/subcategories", response_model=List[DocumentCategoryResponse])
def get_subcategories(
    category_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get subcategories of a category"""
    check_nda_acceptance(user_id)
    
    subcategories = list(document_categories_collection.find({
        "parent_category_id": category_id,
        "is_active": True
    }).sort("sort_order", 1))
    
    for cat in subcategories:
        cat["id"] = str(cat.pop("_id"))
    
    return subcategories


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    category_id: str = Form(...),
    description: Optional[str] = Form(None),
    user_id: str = Depends(get_current_user_id)
):
    """Upload a new document (Admin only)"""
    try:
        result = await DocumentService.upload_document(
            file=file,
            title=title,
            category_id=category_id,
            uploaded_by=user_id,
            description=description
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/category/{category_id}/documents", response_model=List[DocumentResponse])
def list_documents_by_category(
    category_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """List all documents in a category"""
    check_nda_acceptance(user_id)
    check_access_validity(user_id)
    
    documents = list(documents_collection.find({
        "category_id": category_id,
        "is_latest_version": True
    }).sort("uploaded_at", -1))
    
    for doc in documents:
        doc["id"] = str(doc.pop("_id"))
    
    return documents

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get document details"""
    check_nda_acceptance(user_id)
    check_access_validity(user_id)
    
    document = documents_collection.find_one({"_id": ObjectId(document_id)})
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    document["id"] = str(document.pop("_id"))
    return document

@router.get("/{document_id}/download")
async def download_document(
    document_id: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Download a document"""
    # Verify token and get user
    token = credentials.credentials
    payload = AuthService.verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload["sub"]
    
    # Check NDA acceptance
    check_nda_acceptance(user_id)
    
    # Check access validity
    check_access_validity(user_id)
    
    # Check download permission
    if not PermissionService.can_download(user_id):
        raise HTTPException(
            status_code=403,
            detail="You do not have download permissions"
        )
    
    # Get document
    document = documents_collection.find_one({"_id": ObjectId(document_id)})
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    file_path = document["file_path"]
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    
    # Log access
    DocumentService.log_document_access(
        document_id=document_id,
        user_id=user_id,
        action="download",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent", ""),
        access_token=token
    )
    
    return FileResponse(
        path=file_path,
        filename=document["file_name"],
        media_type="application/octet-stream"
    )

@router.get("/{document_id}/view")
async def view_document(
    document_id: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """View document (for PDFs and images)"""
    # Verify token and get user
    token = credentials.credentials
    payload = AuthService.verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload["sub"]
    
    # Check NDA acceptance
    check_nda_acceptance(user_id)
    
    # Check access validity
    check_access_validity(user_id)
    
    # Get document
    document = documents_collection.find_one({"_id": ObjectId(document_id)})
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    file_path = document["file_path"]
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    
    # Log access
    DocumentService.log_document_access(
        document_id=document_id,
        user_id=user_id,
        action="view",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent", ""),
        access_token=token
    )
    
    # Determine media type
    file_type = document["file_type"].lower()
    media_type_map = {
        "pdf": "application/pdf",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif"
    }
    
    media_type = media_type_map.get(file_type, "application/octet-stream")
    
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=document["file_name"]
    )

@router.get("/{document_id}/versions")
def get_document_versions(
    document_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get all versions of a document"""
    check_nda_acceptance(user_id)
    
    from database import document_versions_collection
    
    versions = list(document_versions_collection.find({
        "document_id": document_id
    }).sort("version_number", -1))
    
    for version in versions:
        version["id"] = str(version.pop("_id"))
    
    return versions

@router.get("/{document_id}/access-logs")
def get_document_access_logs(
    document_id: str,
    limit: int = 50
):
    """Get access logs for a document (Admin only)"""
    logs = list(document_access_logs_collection.find({
        "document_id": document_id
    }).sort("accessed_at", -1).limit(limit))
    
    for log in logs:
        log["id"] = str(log.pop("_id"))
    
    return logs
