# from pydantic import BaseModel, EmailStr
# from datetime import datetime
# from typing import Optional
# from enum import Enum

# class AdminRole(str, Enum):
#     SUPER_ADMIN = "super_admin"
#     ADMIN = "admin"
#     USER = "user"

# class AdminCreate(BaseModel):
#     email: EmailStr
#     password: str
#     full_name: str
#     role: AdminRole = AdminRole.USER

# class AdminLogin(BaseModel):
#     email: EmailStr
#     password: str

# class AdminResponse(BaseModel):
#     id: str
#     email: str
#     full_name: str
#     role: str
#     is_active: bool
#     created_at: datetime
#     last_login: Optional[datetime]

# class AdminUpdate(BaseModel):
#     full_name: Optional[str] = None
#     role: Optional[AdminRole] = None
#     is_active: Optional[bool] = None

# class ChangePassword(BaseModel):
#     current_password: str
#     new_password: str

# class TokenResponse(BaseModel):
#     access_token: str
#     token_type: str
#     user: dict

from enum import Enum
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime

# ✅ UNCOMMENT THIS
class AdminRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"

class AdminCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str
    role: AdminRole = AdminRole.USER  # ✅ Use the enum, not string

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class AdminResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: AdminRole  # ✅ Use enum here too
    is_active: bool
    created_at: datetime
    updated_at: datetime

class AdminUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[AdminRole] = None  # ✅ Optional enum
    is_active: Optional[bool] = None


class ChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, description="New password must be at least 8 characters")
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('New password must be at least 8 characters long')
        return v

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict