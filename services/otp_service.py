import pyotp
import secrets
from datetime import datetime, timedelta
from typing import Optional
from database import otp_codes_collection, users_collection
from config import settings
from services.email_service import EmailService

class OTPService:
    @staticmethod
    def generate_otp(email: str) -> tuple[str, datetime]:
        """Generate a 6-digit OTP code"""
        otp_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        
        # Deactivate any existing OTP codes for this email
        otp_codes_collection.update_many(
            {"email": email, "is_used": False},
            {"$set": {"is_used": True}}
        )
        
        # Create new OTP
        otp_data = {
            "email": email,
            "otp_code": otp_code,
            "expires_at": expires_at,
            "is_used": False,
            "attempts": 0,
            "created_at": datetime.utcnow()
        }
        
        otp_codes_collection.insert_one(otp_data)
        
        return otp_code, expires_at
    
    @staticmethod
    def send_otp(email: str) -> bool:
        """Generate and send OTP via email"""
        user = users_collection.find_one({"email": email})
        if not user:
            return False
        
        otp_code, expires_at = OTPService.generate_otp(email)
        
        subject = "Your SAYeTECH Dataroom Login Code"
        body = f"""
        <h2>Your One-Time Password</h2>
        <p>Use this code to log in to the SAYeTECH Investor Dataroom:</p>
        <h1 style="font-size: 32px; letter-spacing: 5px; color: #0066cc;">{otp_code}</h1>
        <p>This code will expire in {settings.OTP_EXPIRY_MINUTES} minutes.</p>
        <p>If you didn't request this code, please ignore this email.</p>
        """
        
        return EmailService.send_email(email, subject, body)
    
    @staticmethod
    def verify_otp(email: str, otp_code: str) -> Optional[dict]:
        """Verify OTP code"""
        otp_doc = otp_codes_collection.find_one({
            "email": email,
            "otp_code": otp_code,
            "is_used": False
        })
        
        if not otp_doc:
            return None
        
        # Check if OTP has expired
        if datetime.utcnow() > otp_doc["expires_at"]:
            otp_codes_collection.update_one(
                {"_id": otp_doc["_id"]},
                {"$set": {"is_used": True}}
            )
            return None
        
        # Check max attempts
        if otp_doc["attempts"] >= settings.OTP_MAX_ATTEMPTS:
            otp_codes_collection.update_one(
                {"_id": otp_doc["_id"]},
                {"$set": {"is_used": True}}
            )
            return None
        
        # Increment attempts
        otp_codes_collection.update_one(
            {"_id": otp_doc["_id"]},
            {"$inc": {"attempts": 1}}
        )
        
        # Mark as used
        otp_codes_collection.update_one(
            {"_id": otp_doc["_id"]},
            {"$set": {"is_used": True}}
        )
        
        # Get user data
        user = users_collection.find_one({"email": email})
        
        # Update last login
        users_collection.update_one(
            {"email": email},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        return {
            "email": email,
            "user_id": str(user["_id"]),
            "full_name": user["full_name"]
        }