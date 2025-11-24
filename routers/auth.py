from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from models.otp import OTPRequest, OTPVerify, OTPResponse
from models.user import UserResponse
from services.otp_service import OTPService
from services.auth_service import AuthService
from database import users_collection
from bson import ObjectId

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security = HTTPBearer()

@router.post("/request-otp", response_model=OTPResponse)
def request_otp(otp_request: OTPRequest):
    """Request OTP for login"""
    user = users_collection.find_one({"email": otp_request.email})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.get("is_active", False):
        raise HTTPException(status_code=403, detail="User account is inactive")
    
    success = OTPService.send_otp(otp_request.email)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send OTP")
    
    return OTPResponse(
        message="OTP sent successfully to your email",
        expires_in_minutes=10
    )

@router.post("/verify-otp")
def verify_otp(otp_verify: OTPVerify):
    """Verify OTP and return access token"""
    result = OTPService.verify_otp(otp_verify.email, otp_verify.otp_code)
    
    if not result:
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")
    
    # Create JWT access token
    token_data = {
        "sub": result["user_id"],
        "email": result["email"],
        "full_name": result["full_name"]
    }
    
    access_token = AuthService.create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": result["user_id"],
            "email": result["email"],
            "full_name": result["full_name"]
        }
    }

@router.get("/me", response_model=UserResponse)
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    token = credentials.credentials
    payload = AuthService.verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = users_collection.find_one({"_id": ObjectId(payload["sub"])})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user["id"] = str(user.pop("_id"))
    return UserResponse(**user)
