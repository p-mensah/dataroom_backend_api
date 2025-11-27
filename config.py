from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    APP_NAME: str = "SAYeTECH Investor Dataroom"
    MONGODB_URL: str = "mongodb+srv://dataroom:dataroom@grow-cohort6.safmckr.mongodb.net/investor_dataroom?retryWrites=true&w=majority"
    DATABASE_NAME: str = "investor_dataroom"
    
     # Brevo (Sendinblue) Configuration
    BREVO_API_KEY: str = "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" 
    BREVO_SENDER_EMAIL: str = "noreply@sayetech.com"
    BREVO_SENDER_NAME: str = "SAYeTECH Dataroom"

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
    
    # File Upload
    UPLOAD_DIR: str = "uploads/documents"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"]
    
    # Redis Cache
    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL: int = 3600  # 1 hour
    
    # Slack Integration
    SLACK_WEBHOOK_URL: str = ""
    
    # Meeting Scheduler
    CALENDLY_API_KEY: str = ""
    
    # Cloudinary Configuration 
    CLOUDINARY_CLOUD_NAME: str = "drqnsoj4r"
    CLOUDINARY_API_KEY: str = "375988834613743"
    CLOUDINARY_API_SECRET: str = "-lGDY543embEy5Oral5slkFer7k"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")



settings = Settings()


