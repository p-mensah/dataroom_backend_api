from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from config import settings
from database import admin_users_collection
from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import bcrypt

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        # Truncate to 72 bytes (critical for bcrypt)
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    payload = AuthService.verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    return payload



# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for storing."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a stored password against one provided by user."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def authenticate_admin(email: str, password: str) -> Optional[dict]:
        """Authenticate admin user."""
        admin = admin_users_collection.find_one({"email": email})
        if not admin:
            return None
        
        if not AuthService.verify_password(password, admin["password_hash"]):
            return None
        
        admin["id"] = str(admin.pop("_id"))
        admin.pop("password_hash")
        return admin
    
    @staticmethod
    def create_admin_user(email: str, password: str, full_name: str) -> dict:
        """Create a new admin user."""
        # Check if admin exists
        existing_admin = admin_users_collection.find_one({"email": email})
        if existing_admin:
            raise ValueError("Admin user already exists")
        
        admin_data = {
            "email": email,
            "password_hash": AuthService.hash_password(password),
            "full_name": full_name,
            "created_at": datetime.utcnow()
        }
        
        result = admin_users_collection.insert_one(admin_data)
        return {"id": str(result.inserted_id), "email": email, "full_name": full_name}
    
    @staticmethod
    def get_admin_by_id(admin_id: str) -> Optional[dict]:
        """Get admin user by ID."""
        try:
            admin = admin_users_collection.find_one({"_id": ObjectId(admin_id)})
            if admin:
                admin["id"] = str(admin.pop("_id"))
                admin.pop("password_hash", None)
                return admin
            return None
        except:
            return None
    
    @staticmethod
    def change_password(admin_id: str, old_password: str, new_password: str) -> bool:
        """Change admin password."""
        try:
            admin = admin_users_collection.find_one({"_id": ObjectId(admin_id)})
            if not admin:
                return False
            
            if not AuthService.verify_password(old_password, admin["password_hash"]):
                return False
            
            new_hash = AuthService.hash_password(new_password)
            admin_users_collection.update_one(
                {"_id": ObjectId(admin_id)},
                {"$set": {"password_hash": new_hash}}
            )
            return True
        except:
            return False