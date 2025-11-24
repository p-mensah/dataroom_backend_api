import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routers import access_requests, admin, auth, nda, permissions, documents, users
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="Secure investor dataroom with OTP authentication, NDA management, and document access control",
    version="2.0.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500, content={"detail": "Internal server error occurred"}
    )


# Include routers
# app.include_router(access_requests.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(nda.router)
app.include_router(permissions.router)
app.include_router(documents.router)
# app.include_router(users.router)


@app.get("/")
def root():
    return {
        "message": "SAYeTECH Investor Dataroom API",
        "version": "2.0.0",
        "features": [
            "OTP Authentication",
            "NDA Management",
            "Role-Based Access Control",
            "Document Management",
            "Audit Logging",
        ],
    }


@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": "2025-01-01T00:00:00Z"}


@app.get("/api/info")
def api_info():
    return {
        "app_name": settings.APP_NAME,
        "database": settings.DATABASE_NAME,
        "otp_expiry_minutes": settings.OTP_EXPIRY_MINUTES,
        "max_file_size_mb": settings.MAX_FILE_SIZE_MB,
        "allowed_file_types": settings.ALLOWED_FILE_TYPES,
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize default data on startup"""
    from services.permission_service import PermissionService
    from services.document_service import DocumentService
    import os

    logger.info("Starting SAYeTECH Investor Dataroom API...")

    # Create upload directory
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    logger.info(f"Upload directory created: {settings.UPLOAD_DIR}")

    # Initialize default permission levels
    PermissionService.create_default_permission_levels()
    logger.info("Default permission levels initialized")

    # Initialize default document categories
    DocumentService.create_default_categories()
    logger.info("Default document categories initialized")

    logger.info("Application startup complete!")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down SAYeTECH Investor Dataroom API...")


# Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000

# ===============================
# init_database.py - Database Initialization Script
# ===============================
"""
Script to initialize the database with default data and admin user
Run this script once after setting up the project:
python init_database.py
"""

from database import (
    admin_users_collection,
    permission_levels_collection,
    document_categories_collection,
)
from services.auth_service import AuthService
from services.permission_service import PermissionService
from services.document_service import DocumentService
from datetime import datetime
import sys


def create_admin_user(email: str, password: str, full_name: str):
    """Create initial admin user"""
    try:
        existing_admin = admin_users_collection.find_one({"email": email})
        if existing_admin:
            print(f"Admin user {email} already exists")
            return

        admin_data = {
            "email": email,
            "password_hash": AuthService.hash_password(password),
            "full_name": full_name,
            "role": "super_admin",
            "created_at": datetime.utcnow(),
            "last_login": None,
        }

        result = admin_users_collection.insert_one(admin_data)
        print(f"✓ Admin user created: {email} (ID: {result.inserted_id})")

    except Exception as e:
        print(f"✗ Error creating admin user: {e}")
        sys.exit(1)


def initialize_permission_levels():
    """Initialize default permission levels"""
    try:
        PermissionService.create_default_permission_levels()
        count = permission_levels_collection.count_documents({})
        print(f"✓ Permission levels initialized: {count} levels")
    except Exception as e:
        print(f"✗ Error initializing permission levels: {e}")


def initialize_document_categories():
    """Initialize default document categories"""
    try:
        DocumentService.create_default_categories()
        count = document_categories_collection.count_documents({})
        print(f"✓ Document categories initialized: {count} categories")
    except Exception as e:
        print(f"✗ Error initializing document categories: {e}")


def main():
    """Main initialization function"""
    print("=" * 60)
    print("SAYeTECH Investor Dataroom - Database Initialization")
    print("=" * 60)
    print()

    # Create admin user
    print("Creating admin user...")
    create_admin_user(
        email="admin@sayetech.com",
        password="Admin@123!",  # Change this in production!
        full_name="SAYeTECH Administrator",
    )
    print()

    # Initialize permission levels
    print("Initializing permission levels...")
    initialize_permission_levels()
    print()

    # Initialize document categories
    print("Initializing document categories...")
    initialize_document_categories()
    print()

    print("=" * 60)
    print("✓ Database initialization complete!")
    print("=" * 60)
    print()
    print("Default Admin Credentials:")
    print("  Email: admin@sayetech.com")
    print("  Password: Admin@123!")
    print()
    print("⚠️  IMPORTANT: Change the admin password immediately!")
    print()


if __name__ == "__main__":
    main()
