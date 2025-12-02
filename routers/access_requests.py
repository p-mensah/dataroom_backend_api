from fastapi import APIRouter, HTTPException
from datetime import datetime
from models.access_request import AccessRequestCreate, AccessRequestResponse
from database import access_requests_collection
from services.email_service import EmailService
from bson import ObjectId

router = APIRouter(prefix="/api/access-requests", tags=["Access Requests"])

@router.post("/", response_model=dict)
def create_access_request(request: AccessRequestCreate):
    """Submit a new access request"""
    
    # Check if email already has a pending request
    existing_request = access_requests_collection.find_one({
        "email": request.email,
        "status": {"$in": ["pending", "approved"]}
    })
    
    if existing_request:
        if existing_request["status"] == "approved":
            raise HTTPException(
                status_code=400,
                detail="You already have an approved access request"
            )
        raise HTTPException(
            status_code=400,
            detail="You already have a pending access request"
        )
    
    # Create request data
    request_data = {
        "email": request.email,
        "full_name": request.full_name, 
        "company": request.company,
        "phone": request.phone,
        "message": request.message,
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "admin_notes": None,
        "otp_verified": False,
        "email_verified": False
    }
    
    # Save to database
    result = access_requests_collection.insert_one(request_data)
    
    # Send confirmation email to user
    try:
        EmailService.send_access_request_confirmation(
            request.email,
            request.full_name
        )
    except Exception as e:
        print(f"Failed to send confirmation email: {e}")
    
    # Send notification to admin
    try:
        EmailService.send_admin_notification(request_data)
    except Exception as e:
        print(f"Failed to send admin notification: {e}")
    
    return {
        "message": "Access request submitted successfully",
        "id": str(result.inserted_id),
        "status": "pending",
        "next_step": "Please check your email for OTP verification"
    }


@router.get("/{request_id}", response_model=dict)
def get_access_request(request_id: str):
    """Get access request status"""
    try:
        request = access_requests_collection.find_one({"_id": ObjectId(request_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid request ID")
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    request["id"] = str(request.pop("_id"))
    request.pop("otp", None)  # Don't expose OTP
    request.pop("otp_expiry", None)
    request.pop("otp_attempts", None)
    
    return request


@router.get("/check/{email}")
def check_access_request_status(email: str):
    """Check if email has an existing access request"""
    request = access_requests_collection.find_one(
        {"email": email},
        sort=[("created_at", -1)]
    )
    
    if not request:
        return {
            "has_request": False,
            "message": "No access request found"
        }
    
    return {
        "has_request": True,
        "status": request["status"],
        "email_verified": request.get("email_verified", False),
        "otp_verified": request.get("otp_verified", False),
        "created_at": request["created_at"],
        "id": str(request["_id"])
    }