# import pyotp
# import secrets
# from datetime import datetime, timedelta
# from typing import Optional
# from database import otp_codes_collection, users_collection
# from config import settings
# from services.email_service import EmailService

# class OTPService:
#     @staticmethod
#     def generate_otp(email: str) -> tuple[str, datetime]:
#         """Generate a 6-digit OTP code"""
#         otp_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
#         expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        
#         # Deactivate any existing OTP codes for this email
#         otp_codes_collection.update_many(
#             {"email": email, "is_used": False},
#             {"$set": {"is_used": True}}
#         )
        
#         # Create new OTP
#         otp_data = {
#             "email": email,
#             "otp_code": otp_code,
#             "expires_at": expires_at,
#             "is_used": False,
#             "attempts": 0,
#             "created_at": datetime.utcnow()
#         }
        
#         otp_codes_collection.insert_one(otp_data)
        
#         return otp_code, expires_at
    
#     @staticmethod
#     def send_otp(email: str) -> bool:
#         """Generate and send OTP via email"""
#         user = users_collection.find_one({"email": email})
#         if not user:
#             return False
        
#         otp_code, expires_at = OTPService.generate_otp(email)
        
#         subject = "Your SAYeTECH Dataroom Login Code"
#         body = f"""
#         <h2>Your One-Time Password</h2>
#         <p>Use this code to log in to the SAYeTECH Investor Dataroom:</p>
#         <h1 style="font-size: 32px; letter-spacing: 5px; color: #0066cc;">{otp_code}</h1>
#         <p>This code will expire in {settings.OTP_EXPIRY_MINUTES} minutes.</p>
#         <p>If you didn't request this code, please ignore this email.</p>
#         """
        
#         return EmailService.send_email(email, subject, body)
    
#     @staticmethod
#     def verify_otp(email: str, otp_code: str) -> Optional[dict]:
#         """Verify OTP code"""
#         otp_doc = otp_codes_collection.find_one({
#             "email": email,
#             "otp_code": otp_code,
#             "is_used": False
#         })
        
#         if not otp_doc:
#             return None
        
#         # Check if OTP has expired
#         if datetime.utcnow() > otp_doc["expires_at"]:
#             otp_codes_collection.update_one(
#                 {"_id": otp_doc["_id"]},
#                 {"$set": {"is_used": True}}
#             )
#             return None
        
#         # Check max attempts
#         if otp_doc["attempts"] >= settings.OTP_MAX_ATTEMPTS:
#             otp_codes_collection.update_one(
#                 {"_id": otp_doc["_id"]},
#                 {"$set": {"is_used": True}}
#             )
#             return None
        
#         # Increment attempts
#         otp_codes_collection.update_one(
#             {"_id": otp_doc["_id"]},
#             {"$inc": {"attempts": 1}}
#         )
        
#         # Mark as used
#         otp_codes_collection.update_one(
#             {"_id": otp_doc["_id"]},
#             {"$set": {"is_used": True}}
#         )
        
#         # Get user data
#         user = users_collection.find_one({"email": email})
        
#         # Update last login
#         users_collection.update_one(
#             {"email": email},
#             {"$set": {"last_login": datetime.utcnow()}}
#         )
        
#         return {
#             "email": email,
#             "user_id": str(user["_id"]),
#             "full_name": user["full_name"]
#         }


import secrets
import string
from datetime import datetime, timedelta
from typing import Optional, Tuple
from database import otp_codes_collection, otp_attempts_collection, investors_collection
from services.brevo_service import BrevoService
from services.auth_service import AuthService
from config import settings
import logging

logger = logging.getLogger(__name__)

class OTPService:
    def __init__(self):
        self.brevo = BrevoService()
    
    @staticmethod
    def generate_otp(length: int = 6) -> str:
        """Generate a random OTP code"""
        return ''.join(secrets.choice(string.digits) for _ in range(length))
    
    def send_otp(self, email: str, purpose: str = "login") -> Tuple[bool, str, Optional[datetime]]:
        """
        Generate and send OTP code
        Returns: (success, message, expires_at)
        """
        # Check if user has exceeded max attempts
        attempts_doc = otp_attempts_collection.find_one({"email": email})
        if attempts_doc:
            if attempts_doc["attempts"] >= settings.OTP_MAX_ATTEMPTS:
                if datetime.utcnow() < attempts_doc["locked_until"]:
                    return False, "Too many attempts. Please try again later.", None
                else:
                    # Reset attempts after lock period
                    otp_attempts_collection.delete_one({"email": email})
        
        # Generate OTP
        otp_code = self.generate_otp(settings.OTP_LENGTH)
        expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        
        # Store OTP in database
        otp_data = {
            "email": email,
            "otp_code": otp_code,
            "purpose": purpose,
            "expires_at": expires_at,
            "created_at": datetime.utcnow(),
            "is_used": False,
            "verified": False
        }
        
        # Delete old OTPs for this email
        otp_codes_collection.delete_many({"email": email, "is_used": False})
        
        # Insert new OTP
        otp_codes_collection.insert_one(otp_data)
        
        # Get user name if exists
        investor = investors_collection.find_one({"email": email})
        name = investor["full_name"] if investor else email.split("@")[0]
        
        # Send OTP via Brevo
        success = self.brevo.send_otp_email(email, otp_code, name)
        
        if success:
            return True, f"OTP sent successfully to {email}", expires_at
        else:
            return False, "Failed to send OTP. Please try again.", None
    
    def verify_otp(self, email: str, otp_code: str) -> Tuple[bool, str, Optional[str]]:
        """
        Verify OTP code
        Returns: (success, message, user_id)
        """
        # Find OTP
        otp_doc = otp_codes_collection.find_one({
            "email": email,
            "otp_code": otp_code,
            "is_used": False
        })
        
        if not otp_doc:
            # Increment failed attempts
            self._increment_failed_attempts(email)
            return False, "Invalid OTP code", None
        
        # Check if expired
        if datetime.utcnow() > otp_doc["expires_at"]:
            otp_codes_collection.update_one(
                {"_id": otp_doc["_id"]},
                {"$set": {"is_used": True}}
            )
            return False, "OTP code has expired", None
        
        # Mark OTP as used
        otp_codes_collection.update_one(
            {"_id": otp_doc["_id"]},
            {"$set": {"is_used": True, "verified": True, "verified_at": datetime.utcnow()}}
        )
        
        # Clear failed attempts
        otp_attempts_collection.delete_one({"email": email})
        
        # Get or create investor
        investor = investors_collection.find_one({"email": email})
        
        if not investor:
            # Create new investor record
            investor_data = {
                "email": email,
                "full_name": email.split("@")[0],
                "company": "Unknown",
                "is_high_value": False,
                "created_at": datetime.utcnow(),
                "last_login": datetime.utcnow()
            }
            result = investors_collection.insert_one(investor_data)
            user_id = str(result.inserted_id)
        else:
            user_id = str(investor["_id"])
            # Update last login
            investors_collection.update_one(
                {"_id": investor["_id"]},
                {"$set": {"last_login": datetime.utcnow()}}
            )
        
        return True, "OTP verified successfully", user_id
    
    def _increment_failed_attempts(self, email: str):
        """Track failed OTP attempts"""
        attempts_doc = otp_attempts_collection.find_one({"email": email})
        
        if attempts_doc:
            new_attempts = attempts_doc["attempts"] + 1
            locked_until = attempts_doc.get("locked_until", datetime.utcnow())
            
            if new_attempts >= settings.OTP_MAX_ATTEMPTS:
                locked_until = datetime.utcnow() + timedelta(minutes=30)
            
            otp_attempts_collection.update_one(
                {"email": email},
                {
                    "$set": {
                        "attempts": new_attempts,
                        "locked_until": locked_until,
                        "last_attempt": datetime.utcnow()
                    }
                }
            )
        else:
            otp_attempts_collection.insert_one({
                "email": email,
                "attempts": 1,
                "locked_until": datetime.utcnow(),
                "last_attempt": datetime.utcnow()
            })
    
    def get_remaining_attempts(self, email: str) -> int:
        """Get remaining OTP attempts"""
        attempts_doc = otp_attempts_collection.find_one({"email": email})
        if not attempts_doc:
            return settings.OTP_MAX_ATTEMPTS
        
        if datetime.utcnow() > attempts_doc.get("locked_until", datetime.utcnow()):
            return settings.OTP_MAX_ATTEMPTS
        
        return max(0, settings.OTP_MAX_ATTEMPTS - attempts_doc["attempts"])