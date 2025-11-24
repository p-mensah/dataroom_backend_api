from fastapi import APIRouter, HTTPException
from datetime import datetime
from models.access_request import AccessRequestCreate, AccessRequestResponse
from database import access_requests_collection
from services.email_service import EmailService
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from typing import Dict
from bson.errors import InvalidId
router = APIRouter(prefix="/api/access-requests", tags=["Access Requests"])



@router.post("/", response_model=dict)
def create_access_request(request: AccessRequestCreate):
    request_data = {
        **request.model_dump(),
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "admin_notes": None
    }
    
    result = access_requests_collection.insert_one(request_data)
    
    # Send emails
    EmailService.send_access_request_confirmation(request.email, request.full_name)
    EmailService.send_admin_notification(request_data)
    
    return {
        "message": "Access request submitted successfully",
        "id": str(result.inserted_id)
    }

@router.get("/{request_id}", response_model=AccessRequestResponse)
def get_access_request(request_id: str):
    """Get an access request by ID"""
    try:
        request = access_requests_collection.find_one({"_id": ObjectId(request_id)})
        if not request:
            raise HTTPException(status_code=404, detail="Access request not found")
        
        request["id"] = str(request.pop("_id"))
        return AccessRequestResponse(**request)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid request ID")