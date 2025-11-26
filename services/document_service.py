import uuid
from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from fastapi import HTTPException, status

from services.cloudinary_service import CloudinaryService
from utils.cloudinary_config import initialize_cloudinary
from database import documents_collection

# Initialize Cloudinary once
initialize_cloudinary()


class DocumentService:
    @staticmethod
    async def upload_document(
        file,
        category_id: str,
        user_id: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        title: Optional[str] = None,
    ):
        # Ensure tags is a list
        if tags is None:
            tags = []

        filename = file.filename
        title = title or filename

        # Read file bytes
        file_bytes = await file.read()

        # Generate unique public ID
        safe_filename = filename.replace(" ", "_").replace(".", "_")
        public_id = f"dataroom_documents/{user_id}/{uuid.uuid4()}_{safe_filename}"

        # Upload to Cloudinary
        upload_result = CloudinaryService.upload_file_from_bytes(
            file_bytes=file_bytes,
            filename=filename,
            public_id=public_id,
            folder="dataroom_documents",
        )

        # Fetch category name (optional: you can enhance this later)
        category_name = "General"

        # Prepare document data for MongoDB
        document_data = {
            "title": title,
            "description": description or "",
            "category_id": category_id,
            "category": category_name,
            "file_path": upload_result["secure_url"],
            "file_type": upload_result["resource_type"],
            "file_size": upload_result["bytes"],
            "uploaded_at": datetime.utcnow(),
            "uploaded_by": user_id,
            "tags": tags,
            "view_count": 0,
            "download_count": 0,
            "cloudinary_public_id": upload_result["public_id"],
            "cloudinary_resource_type": upload_result.get("resource_type", "raw"),
        }

        # Insert into MongoDB
        result = documents_collection.insert_one(document_data)
        document_data["id"] = str(result.inserted_id)
        return document_data

    @staticmethod
    def get_document_url(document_id: str):
        document = documents_collection.find_one({"_id": ObjectId(document_id)})
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document["file_path"]

    @staticmethod
    def delete_document(document_id: str):
        document = documents_collection.find_one({"_id": ObjectId(document_id)})
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        CloudinaryService.delete_file(
            public_id=document["cloudinary_public_id"],
            resource_type=document["cloudinary_resource_type"],
        )

        documents_collection.delete_one({"_id": ObjectId(document_id)})
        return {"message": "Document deleted successfully"}