from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Manages the application's configuration settings.

    This class automatically loads environment variables from a `.env` file,
    allowing for easy customization of application settings.
    """
    APP_NAME: str = "SAYeTECH Investor Dataroom"
    MONGODB_URL: str = "mongodb+srv://dataroom:dataroom@grow-cohort6.safmckr.mongodb.net/"
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
    
    class Config:
        env_file = ".env"

settings = Settings()