from database import admin_users_collection
from services.auth_service import AuthService
from bson import ObjectId
from datetime import datetime
from typing import Optional, List

class AdminService:
    
    @staticmethod
    def create_admin(email: str, password: str, full_name: str, role: str = "user") -> dict:
        """Create a new admin/user (only super admin can create other admins)"""
        # Validate password length
        if len(password.encode('utf-8')) > 72:
            raise ValueError("Password is too long (max 72 bytes)")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Check if user already exists
        existing = admin_users_collection.find_one({"email": email})
        if existing:
            raise ValueError("User with this email already exists")
        
        # Validate role
        valid_roles = ["user", "admin", "super_admin"]
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        
        # Prevent creating super_admin through API (only through script)
        if role == "super_admin":
            raise ValueError("Cannot create super admin through this endpoint")
        
        # Create user
        admin_data = {
            "email": email,
            "password_hash": AuthService.hash_password(password),
            "full_name": full_name,
            "role": role,
            "is_active": True,
            "is_super_admin": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = admin_users_collection.insert_one(admin_data)
        
        return {
            "message": "User created successfully",
            "id": str(result.inserted_id),
            "email": email,
            "full_name": full_name,
            "role": role
        }
    
    @staticmethod
    def authenticate(username_or_email: str, password: str) -> Optional[dict]:
        """Authenticate user by username or email"""
        # Try to find by username first, then email
        user = admin_users_collection.find_one({
            "$or": [
                {"username": username_or_email},
                {"email": username_or_email}
            ]
        })
        
        if not user:
            return None
        
        if not user.get("is_active", False):
            raise ValueError("Account is inactive")
        
        if not AuthService.verify_password(password, user["password_hash"]):
            return None
        
        # Return user data without password
        user["id"] = str(user.pop("_id"))
        user.pop("password_hash", None)
        
        return user
    
    @staticmethod
    def get_admin_by_id(admin_id: str) -> Optional[dict]:
        """Get admin by ID"""
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
    def get_all_admins() -> List[dict]:
        """Get all admins/users"""
        admins = list(admin_users_collection.find())
        
        for admin in admins:
            admin["id"] = str(admin.pop("_id"))
            admin.pop("password_hash", None)
        
        return admins
    
    @staticmethod
    def update_admin(admin_id: str, update_data: dict) -> bool:
        """Update admin data"""
        try:
            # Prevent changing super admin status
            if "is_super_admin" in update_data:
                del update_data["is_super_admin"]
            
            # Prevent downgrading super admin role
            admin = admin_users_collection.find_one({"_id": ObjectId(admin_id)})
            if admin and admin.get("is_super_admin") and "role" in update_data:
                if update_data["role"] != "super_admin":
                    raise ValueError("Cannot change super admin role")
            
            result = admin_users_collection.update_one(
                {"_id": ObjectId(admin_id)},
                {"$set": {**update_data, "updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except:
            return False
    
    @staticmethod
    def delete_admin(admin_id: str) -> bool:
        """Soft delete (deactivate) admin"""
        # Prevent deleting super admin
        admin = admin_users_collection.find_one({"_id": ObjectId(admin_id)})
        if admin and admin.get("is_super_admin"):
            raise ValueError("Cannot delete super admin account")
        
        return AdminService.update_admin(admin_id, {"is_active": False})
    
    @staticmethod
    def change_password(admin_id: str, current_password: str, new_password: str) -> bool:
        """Change admin password"""
        # Validate new password length
        if len(new_password.encode('utf-8')) > 72:
            raise ValueError("New password is too long (max 72 bytes)")
        
        if len(new_password) < 8:
            raise ValueError("New password must be at least 8 characters long")
        
        return AuthService.change_password(admin_id, current_password, new_password)
    
    @staticmethod
    def is_super_admin(role: str) -> bool:
        """Check if role is super admin"""
        return role == "super_admin"
    
    @staticmethod
    def is_admin_or_above(role: str) -> bool:
        """Check if role is admin or super admin"""
        return role in ["admin", "super_admin"]