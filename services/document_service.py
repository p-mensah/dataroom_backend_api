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
        categories: List[str],
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
            "categories": categories,
            "file_path": upload_result["secure_url"],
            "file_url": upload_result["secure_url"],  
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
    def list_documents(
        categories: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        search: Optional[str] = None,
    ):
        """List documents with optional filters"""
        query = {}
        
        if categories:
            query["categories"] = {"$in": categories}
        
        if tags:
            query["tags"] = {"$in": tags}
        
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}},
            ]
        
        documents = list(documents_collection.find(query))
        
        # Convert ObjectId to string and ensure file_url exists
        for doc in documents:
            doc["id"] = str(doc["_id"])
            if "file_url" not in doc and "file_path" in doc:
                doc["file_url"] = doc["file_path"]
        
        return documents

    @staticmethod
    def get_document_by_id(document_id: str):
        """Get a single document by ID"""
        try:
            document = documents_collection.find_one({"_id": ObjectId(document_id)})
            if not document:
                return None
            
            document["id"] = str(document["_id"])
            if "file_url" not in document and "file_path" in document:
                document["file_url"] = document["file_path"]
            
            return document
        except Exception:
            return None

    @staticmethod
    def get_document_url(document_id: str):
        document = documents_collection.find_one({"_id": ObjectId(document_id)})
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document.get("file_url") or document.get("file_path")

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

    @staticmethod
    def get_category_stats():
        """Get document count by category"""
        pipeline = [
            {"$unwind": "$categories"},
            {"$group": {"_id": "$categories", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ]
        
        results = list(documents_collection.aggregate(pipeline))
        
        stats = {
            "total_documents": documents_collection.count_documents({}),
            "by_category": [
                {"category": r["_id"], "count": r["count"]} for r in results
            ],
        }
        
        return stats