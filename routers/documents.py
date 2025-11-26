import os
from typing import List, Optional
from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException, status
from routers.admin_auth import get_current_user  # 
from services.document_service import DocumentService
from models.document import DocumentResponse

router = APIRouter(prefix="/api/documents", tags=["Documents"])


@router.post("/", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    category_id: str = Form(...),
    description: Optional[str] = Form(None),
    tags: List[str] = Form([]),
    current_user: dict = Depends(get_current_user)
):
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
        category_id=category_id,
        user_id=str(current_user["_id"]),
        description=description,
        tags=tags
    )
    
    return result


@router.get("/{document_id}")
async def get_document_url(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):
    url = DocumentService.get_document_url(document_id)
    return {"url": url}


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):
    return DocumentService.delete_document(document_id)