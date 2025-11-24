from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models.user import UserCreate, UserResponse, UserUpdate
from database import users_collection
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/", response_model=dict)
def create_user(user: UserCreate):
    """Create new user (Admin only)"""
    existing = users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    user_data = {
        **user.model_dump(),
        "is_active": True,
        "created_at": datetime.utcnow(),
        "last_login": None
    }
    
    result = users_collection.insert_one(user_data)
    
    return {
        "message": "User created successfully",
        "id": str(result.inserted_id)
    }

@router.get("/", response_model=List[UserResponse])
def list_users(
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
):
    """List all users (Admin only)"""
    query = {}
    if is_active is not None:
        query["is_active"] = is_active
    
    users = list(users_collection.find(query).skip(skip).limit(limit))
    
    for user in users:
        user["id"] = str(user.pop("_id"))
    
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    """Get specific user"""
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user["id"] = str(user.pop("_id"))
    return user

@router.put("/{user_id}")
def update_user(user_id: str, update: UserUpdate):
    """Update user details (Admin only)"""
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = {k: v for k, v in update.model_dump().items() if v is not None}
    
    if update_data:
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
    
    return {"message": "User updated successfully"}

@router.delete("/{user_id}")
def delete_user(user_id: str):
    """Soft delete user (deactivate)"""
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_active": False}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deactivated successfully"}
