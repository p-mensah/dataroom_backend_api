import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import admin, auth, nda, permissions, documents
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
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(nda.router)
app.include_router(permissions.router)
app.include_router(documents.router)


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