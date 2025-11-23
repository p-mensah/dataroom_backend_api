from fastapi import APIRouter, HTTPException
from datetime import datetime
from models.access_request import AccessRequestCreate, AccessRequestResponse
from database import access_requests_collection
from services.email_service import EmailService
from bson import ObjectId

router = APIRouter(prefix="/api/access-requests", tags=["Access Requests"])

@router.post("/", response_model=dict)
def create_access_request(request: AccessRequestCreate):
    """
    Creates a new access request.

    Args:
        request: An `AccessRequestCreate` object containing the request data.

    Returns:
        A dictionary with a success message and the ID of the new request.
    """
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

@router.get("/{request_id}", response_model=dict)
def get_access_request(request_id: str):
    """
    Retrieves a specific access request by its ID.

    Args:
        request_id: The ID of the access request to retrieve.

    Returns:
        The access request data as a dictionary.

    Raises:
        HTTPException: If the request is not found.
    """
    request = access_requests_collection.find_one({"_id": ObjectId(request_id)})
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    request["id"] = str(request.pop("_id"))
    return request