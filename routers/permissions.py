from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.permission import (
    PermissionLevelCreate, 
    PermissionLevelResponse,
    PermissionLevelUpdate
)
from services.permission_service import PermissionService
from database import permission_levels_collection
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/api/permissions", tags=["Permissions"])

@router.get("/levels", response_model=List[PermissionLevelResponse])
def list_permission_levels():
    """Get all permission levels"""
    levels = list(permission_levels_collection.find())
    
    for level in levels:
        level["id"] = str(level.pop("_id"))
    
    return levels

@router.get("/levels/{level_id}", response_model=PermissionLevelResponse)
def get_permission_level(level_id: str):
    """Get specific permission level"""
    level = permission_levels_collection.find_one({"_id": ObjectId(level_id)})
    
    if not level:
        raise HTTPException(status_code=404, detail="Permission level not found")
    
    level["id"] = str(level.pop("_id"))
    return level

@router.post("/levels", response_model=dict)
def create_permission_level(level: PermissionLevelCreate):
    """Create new permission level"""
    existing = permission_levels_collection.find_one({"name": level.name})
    if existing:
        raise HTTPException(status_code=400, detail="Permission level already exists")
    
    level_data = {
        **level.model_dump(),
        "created_at": datetime.utcnow()
    }
    
    result = permission_levels_collection.insert_one(level_data)
    
    return {
        "message": "Permission level created successfully",
        "id": str(result.inserted_id)
    }

@router.put("/levels/{level_id}")
def update_permission_level(level_id: str, update: PermissionLevelUpdate):
    """Update permission level"""
    level = permission_levels_collection.find_one({"_id": ObjectId(level_id)})
    if not level:
        raise HTTPException(status_code=404, detail="Permission level not found")
    
    update_data = {k: v for k, v in update.model_dump().items() if v is not None}
    
    if update_data:
        permission_levels_collection.update_one(
            {"_id": ObjectId(level_id)},
            {"$set": update_data}
        )
    
    return {"message": "Permission level updated successfully"}

@router.delete("/levels/{level_id}")
def delete_permission_level(level_id: str):
    """Delete permission level"""
    result = permission_levels_collection.delete_one({"_id": ObjectId(level_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Permission level not found")
    
    return {"message": "Permission level deleted successfully"}

@router.get("/user/{user_id}/permissions")
def get_user_permissions(user_id: str):
    """Get user's permission details"""
    permissions = PermissionService.get_user_permissions(user_id)
    
    if not permissions:
        raise HTTPException(status_code=404, detail="User permissions not found")
    
    can_download = PermissionService.can_download(user_id)
    access_valid = PermissionService.check_access_expiry(user_id)
    
    return {
        "permissions": permissions,
        "can_download": can_download,
        "access_valid": access_valid
    }
