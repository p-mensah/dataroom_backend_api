
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "SAYeTECH Investor Dataroom"
    MONGODB_URL: str 

    DATABASE_NAME: str = "investor_dataroom"
    
    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    FROM_EMAIL: str = ""
    
    # Admin Configuration
    ADMIN_EMAIL: str = "admin@sayetech.com"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    OTP_EXPIRY_MINUTES: int = 10
    OTP_MAX_ATTEMPTS: int = 3
    
    # File Upload
    MAX_FILE_SIZE_MB: int = 50
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_FILE_TYPES: list = [
        "pdf", "doc", "docx", "xls", "xlsx", 
        "ppt", "pptx", "txt", "csv", "zip"
    ]
    
    # NDA Configuration
    NDA_VERSION: str = "1.0"
    
    class Config:
        env_file = ".env"


settings = Settings()
