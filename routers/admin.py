from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
from typing import List
import secrets
from models.access_request import AccessRequestUpdate
from database import access_requests_collection, access_tokens_collection, audit_logs_collection
from services.email_service import EmailService
from bson import ObjectId
from services.auth_service import AuthService

security = HTTPBearer()

def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verifies the authentication token and returns the current admin user's data.

    Args:
        credentials: The HTTP authorization credentials.

    Returns:
        The admin user's data as a dictionary.

    Raises:
        HTTPException: If the token is invalid or missing.
    """
    token = credentials.credentials
    payload = AuthService.verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return payload

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/access-requests", response_model=List[dict])
def list_access_requests(status: str = None):
    """
    Lists all access requests, optionally filtering by status.

    Args:
        status: The status to filter by (e.g., "pending", "approved").

    Returns:
        A list of access requests.
    """
    query = {"status": status} if status else {}
    requests = list(access_requests_collection.find(query))
    
    for req in requests:
        req["id"] = str(req.pop("_id"))
    
    return requests

@router.put("/access-requests/{request_id}")
def update_access_request(request_id: str, update: AccessRequestUpdate):
    """
    Updates an access request's status and admin notes.

    Args:
        request_id: The ID of the access request to update.
        update: An `AccessRequestUpdate` object containing the update data.

    Returns:
        A dictionary with a success message.

    Raises:
        HTTPException: If the request is not found.
    """
    request = access_requests_collection.find_one({"_id": ObjectId(request_id)})
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    previous_status = request["status"]
    update_data = {
        "status": update.status,
        "updated_at": datetime.utcnow()
    }
    
    if update.admin_notes:
        update_data["admin_notes"] = update.admin_notes
    
    access_requests_collection.update_one(
        {"_id": ObjectId(request_id)},
        {"$set": update_data}
    )
    
    # Log the action
    audit_logs_collection.insert_one({
        "access_request_id": request_id,
        "action": "status_change",
        "previous_status": previous_status,
        "new_status": update.status,
        "notes": update.admin_notes,
        "timestamp": datetime.utcnow()
    })
    
    # Handle status changes
    if update.status == "approved":
        token = secrets.token_urlsafe(32)
        access_tokens_collection.insert_one({
            "access_request_id": request_id,
            "token": token,
            "email": request["email"],
            "expires_at": update.expires_at,
            "is_active": True,
            "created_at": datetime.utcnow()
        })
        EmailService.send_access_approved(request["email"], request["full_name"], token)
    
    elif update.status == "denied":
        EmailService.send_access_denied(
            request["email"], 
            request["full_name"],
            update.admin_notes or ""
        )
    
    return {"message": "Access request updated successfully"}