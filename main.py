import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import the three routers from admin_auth
from routers.admin_auth import admin_auth_router, admin_router, auth_router

# Import other routers directly from their files
from routers.nda import router as nda_router
from routers.permissions import router as permissions_router
from routers.documents import router as documents_router

from config import settings

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
    return JSONResponse(
        status_code=500, content={"detail": "Internal server error occurred"}
    )

# Include routers
app.include_router(admin_auth_router)  # /api/admin-auth/* - Admin authentication (login, register, profile)
app.include_router(admin_router)        # /api/admin/* - Admin management (user CRUD, access requests)
app.include_router(auth_router)         # /api/auth/* - User OTP authentication (request-otp, verify-otp)
app.include_router(nda_router)
app.include_router(permissions_router)
app.include_router(documents_router)

@app.get("/")
def root():
    return {
        "message": "SAYeTECH Investor Dataroom API",
        "version": "2.0.0",
        "features": [
            "Admin Authentication (JWT)",
            "User OTP Authentication",
            "NDA Management",
            "Role-Based Access Control",
            "Document Management",
            "Audit Logging",
        ],
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/info")
def api_info():
    return {
        "app_name": settings.APP_NAME,
        "database": settings.DATABASE_NAME,
        "otp_expiry_minutes": settings.OTP_EXPIRY_MINUTES,
        "max_file_size_mb": settings.MAX_FILE_SIZE_MB,
        "allowed_file_types": settings.ALLOWED_FILE_TYPES,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)