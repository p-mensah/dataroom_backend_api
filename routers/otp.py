from fastapi import APIRouter, HTTPException, Request
from models.otp import OTPRequest, OTPVerify, OTPResponse, OTPVerifyResponse
from services.otp_service import OTPService
from services.auth_service import AuthService
from services.brevo_service import BrevoService
from datetime import datetime

router = APIRouter(prefix="/api/otp", tags=["OTP Authentication"])

otp_service = OTPService()
auth_service = AuthService()
brevo_service = BrevoService()

@router.post("/request", response_model=OTPResponse)
async def request_otp(otp_request: OTPRequest):
    """Request OTP code to be sent via email"""
    success, message, expires_at = otp_service.send_otp(
        otp_request.email,
        otp_request.purpose
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    attempts_remaining = otp_service.get_remaining_attempts(otp_request.email)
    
    return OTPResponse(
        message=message,
        expires_at=expires_at,
        attempts_remaining=attempts_remaining
    )

@router.post("/verify", response_model=OTPVerifyResponse)
async def verify_otp(otp_verify: OTPVerify, request: Request):
    """Verify OTP code and return access token"""
    success, message, user_id = otp_service.verify_otp(
        otp_verify.email,
        otp_verify.otp_code
    )
    
    if not success:
        attempts_remaining = otp_service.get_remaining_attempts(otp_verify.email)
        raise HTTPException(
            status_code=400,
            detail=f"{message}. Attempts remaining: {attempts_remaining}"
        )
    
    # Generate JWT token
    access_token = auth_service.create_access_token(
        data={"user_id": user_id, "email": otp_verify.email}
    )
    
    # Send login success notification
    ip_address = request.client.host
    login_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    brevo_service.send_login_success_email(
        otp_verify.email,
        otp_verify.email.split("@")[0],
        login_time,
        ip_address
    )
    
    return OTPVerifyResponse(
        success=True,
        message="Login successful",
        user_id=user_id,
        access_token=access_token
    )

@router.get("/attempts/{email}")
async def get_remaining_attempts(email: str):
    """Check remaining OTP attempts for an email"""
    attempts_remaining = otp_service.get_remaining_attempts(email)
    
    return {
        "email": email,
        "attempts_remaining": attempts_remaining,
        "max_attempts": settings.OTP_MAX_ATTEMPTS
    }