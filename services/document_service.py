import os
import shutil
from datetime import datetime
from typing import Optional, List
from fastapi import UploadFile
from database import (
    document_categories_collection, 
    documents_collection,
    document_versions_collection,
    document_access_logs_collection,
    users_collection
)
from config import settings
from bson import ObjectId

class DocumentService:
    @staticmethod
    def create_default_categories():
        """Create default document categories"""
        default_categories = [
            {
                "name": "Company Overview",
                "slug": "company-overview",
                "description": "Mission, vision, team, and company structure",
                "parent_category_id": None,
                "sort_order": 1,
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Market & Impact",
                "slug": "market-impact",
                "description": "Market analysis, social impact metrics",
                "parent_category_id": None,
                "sort_order": 2,
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Financials",
                "slug": "financials",
                "description": "Financial statements, projections, cap table",
                "parent_category_id": None,
                "sort_order": 3,
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "name": "IP & Technology",
                "slug": "ip-technology",
                "description": "Patents, technical documentation, R&D",
                "parent_category_id": None,
                "sort_order": 4,
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Traction",
                "slug": "traction",
                "description": "User metrics, partnerships, testimonials",
                "parent_category_id": None,
                "sort_order": 5,
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Legal",
                "slug": "legal",
                "description": "Incorporation documents, contracts, compliance",
                "parent_category_id": None,
                "sort_order": 6,
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]
        
        for category in default_categories:
            existing = document_categories_collection.find_one({"slug": category["slug"]})
            if not existing:
                document_categories_collection.insert_one(category)
    
    @staticmethod
    def validate_file(file: UploadFile) -> tuple[bool, str]:
        """Validate file type and size"""
        # Check file extension
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in settings.ALLOWED_FILE_TYPES:
            return False, f"File type .{file_ext} not allowed"
        
        # Check file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if file_size > max_size_bytes:
            return False, f"File size exceeds {settings.MAX_FILE_SIZE_MB}MB limit"
        
        return True, "Valid"
    
    @staticmethod
    async def upload_document(
        file: UploadFile,
        title: str,
        category_id: str,
        uploaded_by: str,
        description: Optional[str] = None
    ) -> dict:
        """Upload a new document"""
        # Validate file
        is_valid, message = DocumentService.validate_file(file)
        if not is_valid:
            raise ValueError(message)
        
        # Create upload directory if it doesn't exist
        category = document_categories_collection.find_one({"_id": ObjectId(category_id)})
        if not category:
            raise ValueError("Category not found")
        
        category_dir = os.path.join(settings.UPLOAD_DIR, category["slug"])
        os.makedirs(category_dir, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        file_ext = file.filename.split('.')[-1]
        unique_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(category_dir, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Create document record
        document_data = {
            "category_id": category_id,
            "title": title,
            "description": description,
            "file_name": file.filename,
            "file_path": file_path,
            "file_type": file_ext,
            "file_size": file_size,
            "version_number": 1,
            "is_latest_version": True,
            "uploaded_by": uploaded_by,
            "uploaded_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = documents_collection.insert_one(document_data)
        
        # Create initial version record
        version_data = {
            "document_id": str(result.inserted_id),
            "version_number": 1,
            "file_path": file_path,
            "change_description": "Initial upload",
            "uploaded_by": uploaded_by,
            "created_at": datetime.utcnow()
        }
        document_versions_collection.insert_one(version_data)
        
        return {
            "message": "Document uploaded successfully",
            "document_id": str(result.inserted_id)
        }
    
    @staticmethod
    def log_document_access(
        document_id: str,
        user_id: str,
        action: str,
        ip_address: str,
        user_agent: str,
        access_token: str
    ):
        """Log document access"""
        log_data = {
            "document_id": document_id,
            "user_id": user_id,
            "access_token": access_token,
            "action": action,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "accessed_at": datetime.utcnow()
        }
        document_access_logs_collection.insert_one(log_data)