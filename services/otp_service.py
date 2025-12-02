import random
import string
from datetime import datetime, timedelta
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from config import settings
from services.email_service import EmailService

class OTPService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.otp_collection = db.otps
        self.users_collection = db.users
        self.access_requests_collection = db.access_requests
        
    def generate_otp(self, length: int = 6) -> str:
        """Generate a random OTP code"""
        return ''.join(random.choices(string.digits, k=length))
    
    async def create_and_send_otp(self, email: str, purpose: str = "login") -> dict:
        """Create OTP and send via email"""
        
        # Check if email exists based on purpose
        if purpose == "access_request":
            # For access requests, check if there's a pending request
            access_request = await self.access_requests_collection.find_one({"email": email})
            if not access_request:
                return {
                    "success": False,
                    "message": "No access request found for this email. Please submit an access request first."
                }
        else:
            # For login/password reset, check if user exists
            user = await self.users_collection.find_one({"email": email})
            if not user:
                return {
                    "success": False,
                    "message": "User not found"
                }
        
        # Generate OTP
        otp_code = self.generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=10)  # 10 min expiry
        
        # Store OTP in database
        otp_doc = {
            "email": email,
            "otp_code": otp_code,
            "purpose": purpose,
            "created_at": datetime.utcnow(),
            "expires_at": expires_at,
            "verified": False,
            "attempts": 0,
            "max_attempts": 3
        }
        
        # Delete any existing OTPs for this email and purpose
        await self.otp_collection.delete_many({"email": email, "purpose": purpose})
        
        # Insert new OTP
        await self.otp_collection.insert_one(otp_doc)
        
        # Send OTP via email
        subject = f"Your {purpose.replace('_', ' ').title()} OTP - SAYeTECH Dataroom"
        body = f"""
        <html>
        <body>
            <h2>Your OTP Code</h2>
            <p>Your one-time password (OTP) is:</p>
            <h1 style="color: #4CAF50; font-size: 32px; letter-spacing: 5px;">{otp_code}</h1>
            <p>This code will expire in 10 minutes.</p>
            <p>If you didn't request this code, please ignore this email.</p>
            <br>
            <p>Best regards,<br>SAYeTECH Team</p>
        </body>
        </html>
        """
        
        email_sent = EmailService.send_email(email, subject, body)
        
        if not email_sent:
            return {
                "success": False,
                "message": "Failed to send OTP email"
            }
        
        return {
            "success": True,
            "message": f"OTP sent to {email}",
            "expires_at": expires_at,
            "attempts_remaining": 3
        }
    
    async def verify_otp(self, email: str, otp_code: str, purpose: str = "login") -> dict:
        """Verify OTP code"""
        
        # Find OTP
        otp_doc = await self.otp_collection.find_one({
            "email": email,
            "purpose": purpose,
            "verified": False
        })
        
        if not otp_doc:
            return {
                "success": False,
                "message": "No valid OTP found. Please request a new one."
            }
        
        # Check if expired
        if datetime.utcnow() > otp_doc["expires_at"]:
            await self.otp_collection.delete_one({"_id": otp_doc["_id"]})
            return {
                "success": False,
                "message": "OTP has expired. Please request a new one."
            }
        
        # Check attempts
        if otp_doc["attempts"] >= otp_doc["max_attempts"]:
            await self.otp_collection.delete_one({"_id": otp_doc["_id"]})
            return {
                "success": False,
                "message": "Maximum attempts exceeded. Please request a new OTP."
            }
        
        # Verify OTP
        if otp_doc["otp_code"] != otp_code:
            # Increment attempts
            await self.otp_collection.update_one(
                {"_id": otp_doc["_id"]},
                {"$inc": {"attempts": 1}}
            )
            remaining = otp_doc["max_attempts"] - otp_doc["attempts"] - 1
            return {
                "success": False,
                "message": f"Invalid OTP. {remaining} attempts remaining."
            }
        
        # OTP is valid - mark as verified
        await self.otp_collection.update_one(
            {"_id": otp_doc["_id"]},
            {"$set": {"verified": True}}
        )
        
        response = {
            "success": True,
            "message": "OTP verified successfully"
        }
        
        # Add additional data based on purpose
        if purpose == "access_request":
            access_request = await self.access_requests_collection.find_one({"email": email})
            if access_request:
                response["access_request_id"] = str(access_request["_id"])
        else:
            user = await self.users_collection.find_one({"email": email})
            if user:
                response["user_id"] = str(user["_id"])
                # You can generate access token here if needed
        
        return response