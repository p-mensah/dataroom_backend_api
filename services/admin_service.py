# from typing import Optional, List
# from datetime import datetime
# from bson import ObjectId
# from database import admin_users_collection, users_collection
# from services.auth_service import AuthService
# from models.admin import AdminRole

# class AdminService:
#     @staticmethod
#     def create_admin(email: str, password: str, full_name: str, 
#                      role: str = "user") -> dict:
#         """Create a new admin/user account"""
#         # Check if user exists
#         existing = admin_users_collection.find_one({"email": email})
#         if existing:
#             raise ValueError("User with this email already exists")
        
#         # Validate role
#         valid_roles = ["super_admin", "admin", "user"]
#         if role not in valid_roles:
#             raise ValueError(f"Invalid role. Must be one of: {valid_roles}")
        
#         # Create admin user
#         admin_data = {
#             "email": email,
#             "password_hash": AuthService.hash_password(password),
#             "full_name": full_name,
#             "role": role,
#             "is_active": True,
#             "created_at": datetime.utcnow(),
#             "last_login": None
#         }
        
#         result = admin_users_collection.insert_one(admin_data)
        
#         return {
#             "id": str(result.inserted_id),
#             "email": email,
#             "full_name": full_name,
#             "role": role,
#             "message": f"{role.replace('_', ' ').title()} account created successfully"
#         }
    
#     @staticmethod
#     def authenticate(email: str, password: str) -> Optional[dict]:
#         """Authenticate admin/user and return user data"""
#         admin = admin_users_collection.find_one({"email": email})
        
#         if not admin:
#             return None
        
#         if not admin.get("is_active", False):
#             raise ValueError("Account is inactive")
        
#         if not AuthService.verify_password(password, admin["password_hash"]):
#             return None
        
#         # Update last login
#         admin_users_collection.update_one(
#             {"_id": admin["_id"]},
#             {"$set": {"last_login": datetime.utcnow()}}
#         )
        
#         return {
#             "id": str(admin["_id"]),
#             "email": admin["email"],
#             "full_name": admin["full_name"],
#             "role": admin["role"]
#         }
    
#     @staticmethod
#     def get_admin_by_id(admin_id: str) -> Optional[dict]:
#         """Get admin by ID"""
#         admin = admin_users_collection.find_one({"_id": ObjectId(admin_id)})
        
#         if not admin:
#             return None
        
#         admin["id"] = str(admin.pop("_id"))
#         admin.pop("password_hash", None)
#         return admin
    
#     @staticmethod
#     def get_all_admins() -> List[dict]:
#         """Get all admin users"""
#         admins = list(admin_users_collection.find())
        
#         for admin in admins:
#             admin["id"] = str(admin.pop("_id"))
#             admin.pop("password_hash", None)
        
#         return admins
    
#     @staticmethod
#     def update_admin(admin_id: str, update_data: dict) -> bool:
#         """Update admin details"""
#         if not update_data:
#             return False
        
#         result = admin_users_collection.update_one(
#             {"_id": ObjectId(admin_id)},
#             {"$set": update_data}
#         )
        
#         return result.modified_count > 0
    
#     @staticmethod
#     def change_password(admin_id: str, current_password: str, 
#                        new_password: str) -> bool:
#         """Change admin password"""
#         admin = admin_users_collection.find_one({"_id": ObjectId(admin_id)})
        
#         if not admin:
#             raise ValueError("User not found")
        
#         if not AuthService.verify_password(current_password, admin["password_hash"]):
#             raise ValueError("Current password is incorrect")
        
#         new_hash = AuthService.hash_password(new_password)
        
#         result = admin_users_collection.update_one(
#             {"_id": ObjectId(admin_id)},
#             {"$set": {"password_hash": new_hash}}
#         )
        
#         return result.modified_count > 0
    
#     @staticmethod
#     def delete_admin(admin_id: str) -> bool:
#         """Soft delete admin (deactivate)"""
#         result = admin_users_collection.update_one(
#             {"_id": ObjectId(admin_id)},
#             {"$set": {"is_active": False}}
#         )
        
#         return result.modified_count > 0
    
#     @staticmethod
#     def check_permission(user_role: str, required_role: str) -> bool:
#         """Check if user has required permission level"""
#         role_hierarchy = {
#             "super_admin": 3,
#             "admin": 2,
#             "user": 1
#         }
        
#         user_level = role_hierarchy.get(user_role, 0)
#         required_level = role_hierarchy.get(required_role, 0)
        
#         return user_level >= required_level
    
#     @staticmethod
#     def is_super_admin(user_role: str) -> bool:
#         """Check if user is super admin"""
#         return user_role == "super_admin"
    
#     @staticmethod
#     def is_admin_or_above(user_role: str) -> bool:
#         """Check if user is admin or super admin"""
#         return user_role in ["admin", "super_admin"]


from passlib.context import CryptContext
from database import admin_users_collection
from bson import ObjectId
from datetime import datetime
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminService:
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password with bcrypt.
        Bcrypt has a 72-byte limit, so we pre-hash long passwords with SHA256
        """
        # If password is longer than 72 bytes, pre-hash it with SHA256
        if len(password.encode('utf-8')) > 72:
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        # Apply same pre-hashing if password is too long
        if len(plain_password.encode('utf-8')) > 72:
            plain_password = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
        
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Validate password requirements:
        - At least 8 characters
        - Accept any characters (letters, numbers, special characters)
        """
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        return True
    
    @staticmethod
    def create_admin(email: str, password: str, full_name: str, role: str = "user"):
        """Create a new admin/user"""
        # Validate password
        AdminService.validate_password(password)
        
        # Check if user already exists
        existing_user = admin_users_collection.find_one({"email": email})
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Validate role
        valid_roles = ["user", "admin", "super_admin"]
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        
        # Create user document
        user_data = {
            "email": email,
            "password": AdminService.hash_password(password),
            "full_name": full_name,
            "role": role,
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = admin_users_collection.insert_one(user_data)
        
        return {
            "message": "User created successfully",
            "id": str(result.inserted_id)
        }
    
    @staticmethod
    def authenticate(email: str, password: str):
        """Authenticate user with email and password"""
        user = admin_users_collection.find_one({"email": email})
        
        if not user:
            return None
        
        if not user.get("is_active", False):
            raise ValueError("Account is inactive")
        
        if not AdminService.verify_password(password, user["password"]):
            return None
        
        # Return user data without password
        user["id"] = str(user.pop("_id"))
        user.pop("password")
        
        return user
    
    @staticmethod
    def get_admin_by_id(admin_id: str):
        """Get admin by ID"""
        try:
            user = admin_users_collection.find_one({"_id": ObjectId(admin_id)})
            
            if user:
                user["id"] = str(user.pop("_id"))
                user.pop("password", None)
            
            return user
        except Exception:
            return None
    
    @staticmethod
    def get_all_admins():
        """Get all admins"""
        users = list(admin_users_collection.find())
        
        for user in users:
            user["id"] = str(user.pop("_id"))
            user.pop("password", None)
        
        return users
    
    @staticmethod
    def update_admin(admin_id: str, update_data: dict):
        """Update admin details"""
        try:
            # Don't allow password update through this method
            update_data.pop("password", None)
            update_data["updated_at"] = datetime.utcnow()
            
            result = admin_users_collection.update_one(
                {"_id": ObjectId(admin_id)},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
        except Exception:
            return False
    
    @staticmethod
    def change_password(admin_id: str, current_password: str, new_password: str):
        """Change user password"""
        # Validate new password
        AdminService.validate_password(new_password)
        
        user = admin_users_collection.find_one({"_id": ObjectId(admin_id)})
        
        if not user:
            raise ValueError("User not found")
        
        # Verify current password
        if not AdminService.verify_password(current_password, user["password"]):
            raise ValueError("Current password is incorrect")
        
        # Update password
        result = admin_users_collection.update_one(
            {"_id": ObjectId(admin_id)},
            {
                "$set": {
                    "password": AdminService.hash_password(new_password),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def delete_admin(admin_id: str):
        """Soft delete (deactivate) admin"""
        try:
            result = admin_users_collection.update_one(
                {"_id": ObjectId(admin_id)},
                {
                    "$set": {
                        "is_active": False,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            return result.modified_count > 0
        except Exception:
            return False
    
    @staticmethod
    def is_super_admin(role: str) -> bool:
        """Check if role is super admin"""
        return role == "super_admin"
    
    @staticmethod
    def is_admin_or_above(role: str) -> bool:
        """Check if role is admin or super admin"""
        return role in ["admin", "super_admin"]