
# from pydantic import BaseModel, EmailStr
# from datetime import datetime
# from typing import Optional

# class OTPRequest(BaseModel):
#     email: EmailStr
#     purpose: str = "login"  # login, password_reset, verify_email

# class OTPVerify(BaseModel):
#     email: EmailStr
#     otp_code: str

# class OTPResponse(BaseModel):
#     message: str
#     expires_at: datetime
#     attempts_remaining: int

# class OTPVerifyResponse(BaseModel):
#     success: bool
#     message: str
#     user_id: Optional[str] = None
#     access_token: Optional[str] = None

# class OTPCreate(BaseModel):
#     email: str
#     otp: str


from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class OTPRequest(BaseModel):
    email: EmailStr
    purpose: str = "login"  # login, password_reset, verify_email, access_request

class OTPVerify(BaseModel):
    email: EmailStr
    otp_code: str
    purpose: str = "login"  # Add purpose to verification

class OTPResponse(BaseModel):
    message: str
    expires_at: datetime
    attempts_remaining: int

class OTPVerifyResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[str] = None
    access_token: Optional[str] = None
    access_request_id: Optional[str] = None  # Add this for access requests

class OTPCreate(BaseModel):
    email: str
    otp: str
    purpose: str = "login"