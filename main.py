import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers.access_requests import router as access_requests_router
from routers.admin import router as admin_router

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(access_requests_router)
app.include_router(admin_router)

@app.get("/")
def root():
    """
    Returns a welcome message for the API root.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "SAYeTECH Investor Dataroom API"}

@app.get("/health")
def health():
    """
    Returns the health status of the API.

    Returns:
        dict: A dictionary containing the health status.
    """
    return {"status": "healthy"}