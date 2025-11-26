
# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime

# class OTPCreate(BaseModel):
#     email: str
#     purpose: str  # e.g., "verify_email", "reset_password", "2fa"

# class OTPVerify(BaseModel):
#     email: str
#     otp_code: str

# class OTPResponse(BaseModel):
#     id: str
#     email: str
#     purpose: str
#     expires_at: datetime
#     verified: bool = False

# class OTPRequest(BaseModel):  # Add this class
#     email: str

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class OTPRequest(BaseModel):
    email: EmailStr
    purpose: str = "login"  # login, password_reset, verify_email

class OTPVerify(BaseModel):
    email: EmailStr
    otp_code: str

class OTPResponse(BaseModel):
    message: str
    expires_at: datetime
    attempts_remaining: int

class OTPVerifyResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[str] = None
    access_token: Optional[str] = None

class OTPCreate(BaseModel):
    email: str
    otp: str