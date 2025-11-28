import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import admin_users_collection
from services.auth_service import AuthService
from datetime import datetime

def create_super_admin():
    """Create the root super admin account"""
    
    # Check if super admin already exists
    existing_super_admin = admin_users_collection.find_one({"email": "root@sayetech.com"})
    
    if existing_super_admin:
        print(" Super admin already exists")
        print(f"   Username: root")
        print(f"   Email: root@sayetech.com")
        return
    
    # Create super admin
    super_admin_data = {
        "email": "root@sayetech.com",
        "username": "root",
        "password_hash": AuthService.hash_password("admin@admin"),
        "full_name": "Super Administrator",
        "role": "super_admin",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "is_super_admin": True  # Special flag
    }
    
    result = admin_users_collection.insert_one(super_admin_data)
    
    print(" Super admin created successfully!")
    print(f"   Username: root")
    print(f"   Email: root@sayetech.com")
    print(f"   Password: admin@admin")
    print(f"   ID: {result.inserted_id}")
    print("\n⚠️  IMPORTANT: Change the password after first login!")

if __name__ == "__main__":
    create_super_admin()