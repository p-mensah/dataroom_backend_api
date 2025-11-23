from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from config import settings
from database import admin_users_collection
from bson import ObjectId

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

class AuthService:
    """
    Provides authentication and authorization services.
    """
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a password for storing.

        Args:
            password: The password to hash.

        Returns:
            The hashed password.
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a stored password against one provided by the user.

        Args:
            plain_password: The password to verify.
            hashed_password: The hashed password to compare against.

        Returns:
            True if the passwords match, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Creates a JWT access token.

        Args:
            data: The data to encode in the token.
            expires_delta: The optional expiration time for the token.

        Returns:
            The encoded JWT access token.
        """
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
        """
        Verifies and decodes a JWT token.

        Args:
            token: The JWT token to verify.

        Returns:
            The decoded token payload if verification is successful, otherwise None.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def authenticate_admin(email: str, password: str) -> Optional[dict]:
        """
        Authenticates an admin user.

        Args:
            email: The admin's email.
            password: The admin's password.

        Returns:
            The admin's data if authentication is successful, otherwise None.
        """
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
        """
        Creates a new admin user.

        Args:
            email: The new admin's email.
            password: The new admin's password.
            full_name: The new admin's full name.

        Returns:
            A dictionary containing the new admin's ID, email, and full name.

        Raises:
            ValueError: If an admin with the same email already exists.
        """
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
        """
        Gets an admin user by their ID.

        Args:
            admin_id: The ID of the admin to retrieve.

        Returns:
            The admin's data if found, otherwise None.
        """
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
        """
        Changes an admin's password.

        Args:
            admin_id: The ID of the admin whose password is to be changed.
            old_password: The admin's current password.
            new_password: The new password.

        Returns:
            True if the password was successfully changed, False otherwise.
        """
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