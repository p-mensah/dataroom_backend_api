from datetime import datetime
from typing import Optional, List
from database import permission_levels_collection, users_collection, access_tokens_collection
from bson import ObjectId

class PermissionService:
    @staticmethod
    def create_default_permission_levels():
        """Create default permission levels"""
        default_levels = [
            {
                "name": "View Only",
                "description": "Can only view documents, no download",
                "can_view": True,
                "can_download": False,
                "has_expiry": False,
                "max_downloads": None,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Download Allowed",
                "description": "Can view and download documents",
                "can_view": True,
                "can_download": True,
                "has_expiry": False,
                "max_downloads": None,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Expiry-Controlled",
                "description": "Access expires after set date",
                "can_view": True,
                "can_download": True,
                "has_expiry": True,
                "max_downloads": 10,
                "created_at": datetime.utcnow()
            }
        ]
        
        for level in default_levels:
            existing = permission_levels_collection.find_one({"name": level["name"]})
            if not existing:
                permission_levels_collection.insert_one(level)
    
    @staticmethod
    def get_user_permissions(user_id: str) -> Optional[dict]:
        """Get user's permission level"""
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user or "permission_level_id" not in user:
            return None
        
        permission = permission_levels_collection.find_one({
            "_id": ObjectId(user["permission_level_id"])
        })
        
        if permission:
            permission["id"] = str(permission.pop("_id"))
        
        return permission
    
    @staticmethod
    def can_download(user_id: str) -> bool:
        """Check if user can download documents"""
        permissions = PermissionService.get_user_permissions(user_id)
        if not permissions:
            return False
        
        return permissions.get("can_download", False)
    
    @staticmethod
    def check_access_expiry(user_id: str) -> bool:
        """Check if user's access has expired"""
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return False
        
        permissions = PermissionService.get_user_permissions(user_id)
        if not permissions or not permissions.get("has_expiry"):
            return True
        
        # Check token expiry
        token = access_tokens_collection.find_one({
            "email": user["email"],
            "is_active": True
        })
        
        if not token:
            return False
        
        expires_at = token.get("expires_at")
        if expires_at and datetime.utcnow() > expires_at:
            access_tokens_collection.update_one(
                {"_id": token["_id"]},
                {"$set": {"is_active": False}}
            )
            users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"is_active": False}}
            )
            return False
        
        return True
    
    @staticmethod
    def update_user_permission(user_id: str, permission_level_id: str) -> bool:
        """Update user's permission level"""
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"permission_level_id": permission_level_id}}
        )
        return result.modified_count > 0