import os
import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from bson import ObjectId
from datetime import datetime

from models.document import (
    DocumentCategoryCreate,
    DocumentCategoryResponse,
    DocumentUpload,
    DocumentResponse,
    DocumentCategory
)
from services.document_service import DocumentService
from services.permission_service import PermissionService
from services.nda_service import NDAService
from services.auth_service import AuthService
from database import (
    document_categories_collection,
    documents_collection,
    document_access_logs_collection,
    admin_users_collection,
    users_collection
)

router = APIRouter(prefix="/api/documents", tags=["Documents"])
security = HTTPBearer()


def get_current_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extract user from JWT token - supports both admin and regular users"""
    token = credentials.credentials
    payload = AuthService.verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload["sub"]
    
    # First check if it's an admin user
    admin_user = admin_users_collection.find_one({"_id": ObjectId(user_id)})
    if admin_user:
        return {
            "id": str(admin_user["_id"]),
            "_id": admin_user["_id"],
            "email": admin_user["email"],
            "full_name": admin_user["full_name"],
            "role": admin_user.get("role", "admin"),
            "is_admin": True,
            "is_active": admin_user.get("is_active", True)
        }
    
    # Then check regular users
    regular_user = users_collection.find_one({"_id": ObjectId(user_id)})
    if regular_user:
        return {
            "id": str(regular_user["_id"]),
            "_id": regular_user["_id"],
            "email": regular_user["email"],
            "full_name": regular_user["full_name"],
            "role": "user",
            "is_admin": False,
            "is_active": regular_user.get("is_active", True)
        }
    
    raise HTTPException(status_code=404, detail="User not found")

get_current_user = get_current_user_from_token

def check_nda_acceptance(user_data: dict):
    """Middleware to check NDA acceptance (skip for admins)"""
    if user_data.get("is_admin"):
        return
    
    if not NDAService.has_accepted_nda(user_data["id"]):
        raise HTTPException(
            status_code=403, 
            detail="NDA must be accepted before accessing documents"
        )

def check_access_validity(user_data: dict):
    """Check if user's access is still valid (skip for admins)"""
    if user_data.get("is_admin"):
        return
    
    if not PermissionService.check_access_expiry(user_data["id"]):
        raise HTTPException(
            status_code=403,
            detail="Access has expired"
        )

def require_admin(user_data: dict = Depends(get_current_user_from_token)):
    """Require admin role"""
    if not user_data.get("is_admin"):
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return user_data


# Document Categories Endpoints
@router.get("/categories/list")
async def get_categories_list():
    """Get list of available document categories (enum values)"""
    return {
        "categories": [
            {"value": cat.value, "label": cat.value} 
            for cat in DocumentCategory
        ]
    }

@router.post("/", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    categories: str = Form(...),
    description: Optional[str] = Form(None),
    tags: str = Form("[]"),
    current_user: dict = Depends(require_admin)
):
    """
    Upload a document with multiple categories (Admin only)
    
    - **file**: The document file to upload
    - **categories**: JSON array or comma-separated (e.g., ["Company Overview", "Financials"])
    - **description**: Optional description
    - **tags**: JSON array or comma-separated (e.g., ["Q4", "2024"])
    """
    # Parse categories - support both JSON and comma-separated
    try:
        if categories.strip().startswith('['):
            categories_list = json.loads(categories)
        else:
            categories_list = [cat.strip() for cat in categories.split(',') if cat.strip()]
        
        if not isinstance(categories_list, list):
            categories_list = [str(categories_list)]
        
        if not categories_list:
            raise ValueError("At least one category is required")
        if len(categories_list) > 3:
            raise ValueError("Maximum 3 categories allowed")
            
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid categories format: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Validate categories
    valid_categories = [cat.value for cat in DocumentCategory]
    for cat in categories_list:
        if cat not in valid_categories:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid category: '{cat}'. Valid: {', '.join(valid_categories)}"
            )
    
    # Parse tags
    tags_list = []
    if tags and tags.strip():
        try:
            if tags.strip().startswith('['):
                tags_list = json.loads(tags)
            else:
                tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            
            if not isinstance(tags_list, list):
                tags_list = [str(tags_list)]
        except json.JSONDecodeError:
            tags_list = []
    
    # Validate file type
    allowed_types = [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv", ".zip"]
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_extension} not allowed"
        )

    # Upload using the service
    result = await DocumentService.upload_document(
        file=file,
        categories=categories_list,
        user_id=str(current_user["_id"]),
        description=description or "",
        tags=tags_list
    )
    
    return result


# Document Listing & Search

@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    categories: Optional[str] = None,
    tags: Optional[str] = None,
    search: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    List all documents with optional filters
    
    - **categories**: Comma-separated (e.g., "Financials,Legal")
    - **tags**: Comma-separated
    - **search**: Search in title and description
    """
    if not current_user.get("is_admin"):
        check_nda_acceptance(current_user)
        check_access_validity(current_user)
    
    categories_list = None
    if categories:
        categories_list = [cat.strip() for cat in categories.split(",") if cat.strip()]
    
    tags_list = None
    if tags:
        tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    
    documents = DocumentService.list_documents(
        categories=categories_list,
        tags=tags_list,
        search=search
    )
    
    return documents

@router.get("/by-category/{category}")
async def get_documents_by_category(
    category: str,
    current_user: dict = Depends(get_current_user)
):
    """Get all documents in a specific category by name"""
    if not current_user.get("is_admin"):
        check_nda_acceptance(current_user)
        check_access_validity(current_user)
    
    # Validate category
    valid_categories = [cat.value for cat in DocumentCategory]
    if category not in valid_categories:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category. Valid: {', '.join(valid_categories)}"
        )
    
    documents = DocumentService.list_documents(categories=[category])
    
    return {
        "category": category,
        "count": len(documents),
        "documents": documents
    }


# Document Retrieval

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific document by ID"""
    if not current_user.get("is_admin"):
        check_nda_acceptance(current_user)
        check_access_validity(current_user)
    
    document = DocumentService.get_document_by_id(document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return document

@router.get("/{document_id}/url")
async def get_document_url(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get document download URL"""
    if not current_user.get("is_admin"):
        check_nda_acceptance(current_user)
        check_access_validity(current_user)
    
    url = DocumentService.get_document_url(document_id)
    
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return {"url": url, "document_id": document_id}

@router.get("/{document_id}/download")
async def download_document(
    document_id: str,
    request: Request,
    user_data: dict = Depends(get_current_user)
):
    """Download a document"""
    if not user_data.get("is_admin"):
        check_nda_acceptance(user_data)
        check_access_validity(user_data)
        
        if not PermissionService.can_download(user_data["id"]):
            raise HTTPException(
                status_code=403,
                detail="You do not have download permissions"
            )
    
    document = documents_collection.find_one({"_id": ObjectId(document_id)})
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # For Cloudinary URLs, redirect to the URL
    file_url = document.get("file_url") or document.get("file_path")
    
    # Log access
    DocumentService.log_document_access(
        document_id=document_id,
        user_id=user_data["id"],
        action="download",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent", "")
    )
    
    # Redirect to Cloudinary URL
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=file_url)

# Document Management


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: dict = Depends(require_admin)
):
    """Delete a document (Admin only)"""
    result = DocumentService.delete_document(document_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return {"message": "Document deleted successfully", "document_id": document_id}

@router.put("/{document_id}")
async def update_document(
    document_id: str,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    categories: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    user_data: dict = Depends(require_admin)
):
    """Update document metadata (Admin only)"""
    document = documents_collection.find_one({"_id": ObjectId(document_id)})
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    update_data = {}
    
    if title:
        update_data["title"] = title
    if description:
        update_data["description"] = description
    
    if categories:
        try:
            if categories.strip().startswith('['):
                categories_list = json.loads(categories)
            else:
                categories_list = [cat.strip() for cat in categories.split(',')]
            
            if len(categories_list) > 3:
                raise ValueError("Maximum 3 categories")
            
            # Validate
            valid_categories = [cat.value for cat in DocumentCategory]
            for cat in categories_list:
                if cat not in valid_categories:
                    raise ValueError(f"Invalid category: {cat}")
            
            update_data["categories"] = categories_list
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    if tags:
        try:
            if tags.strip().startswith('['):
                tags_list = json.loads(tags)
            else:
                tags_list = [tag.strip() for tag in tags.split(',')]
            update_data["tags"] = tags_list
        except json.JSONDecodeError:
            pass
    
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        documents_collection.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": update_data}
        )
        return {"message": "Document updated successfully"}
    
    raise HTTPException(status_code=400, detail="No updates provided")


# Statistics & Admin


@router.get("/stats/by-category")
async def get_category_stats(
    current_user: dict = Depends(require_admin)
):
    """Get document count statistics by category (Admin only)"""
    stats = DocumentService.get_category_stats()
    return stats

@router.get("/{document_id}/access-logs")
def get_document_access_logs(
    document_id: str,
    limit: int = 50,
    user_data: dict = Depends(require_admin)
):
    """Get access logs for a document (Admin only)"""
    logs = list(document_access_logs_collection.find({
        "document_id": document_id
    }).sort("accessed_at", -1).limit(limit))
    
    for log in logs:
        log["id"] = str(log.pop("_id"))
    
    return logs