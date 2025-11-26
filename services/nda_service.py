# from datetime import datetime
# from typing import Optional
# from database import nda_acceptances_collection, users_collection
# from config import settings
# from bson import ObjectId

# class NDAService:
#     @staticmethod
#     def get_nda_content() -> dict:
#         """Get current NDA content"""
#         return {
#             "title": "Non-Disclosure Agreement",
#             "version": "1.0", # settings.NDA_VERSION,
#             "content": """
# NON-DISCLOSURE AGREEMENT

# This Non-Disclosure Agreement ("Agreement") is entered into as of the date of acceptance 
# between SAYeTECH ("Disclosing Party") and the undersigned ("Receiving Party").

# 1. CONFIDENTIAL INFORMATION
# The Receiving Party acknowledges that all information, documents, data, and materials 
# provided through the SAYeTECH Investor Dataroom constitute confidential and proprietary 
# information.

# 2. OBLIGATIONS
# The Receiving Party agrees to:
# - Maintain strict confidentiality of all information received
# - Use the information solely for evaluation purposes
# - Not disclose information to any third party without written consent
# - Return or destroy all confidential information upon request

# 3. TERM
# This Agreement shall remain in effect for a period of 5 years from the date of acceptance.

# 4. REMEDIES
# The Receiving Party acknowledges that breach of this Agreement may cause irreparable harm 
# and that monetary damages may be inadequate.

# By digitally signing below, you acknowledge that you have read, understood, and agree to 
# be bound by the terms of this Non-Disclosure Agreement.
#             """,
#             "effective_date": datetime.utcnow()
#         }
    
#     @staticmethod
#     def accept_nda(user_id: str, digital_signature: str, ip_address: str, 
#                    user_agent: str) -> dict:
#         """Record NDA acceptance"""
#         user = users_collection.find_one({"_id": ObjectId(user_id)})
#         if not user:
#             raise ValueError("User not found")
        
#         # Check if user has already accepted current NDA version
#         existing_acceptance = nda_acceptances_collection.find_one({
#             "user_id": user_id,
#             "nda_version": settings.NDA_VERSION,
#             "is_active": True
#         })
        
#         if existing_acceptance:
#             return {
#                 "message": "NDA already accepted",
#                 "acceptance_id": str(existing_acceptance["_id"])
#             }
        
#         # Create new acceptance record
#         acceptance_data = {
#             "user_id": user_id,
#             "nda_version": settings.NDA_VERSION,
#             "digital_signature": digital_signature,
#             "ip_address": ip_address,
#             "user_agent": user_agent,
#             "accepted_at": datetime.utcnow(),
#             "is_active": True
#         }
        
#         result = nda_acceptances_collection.insert_one(acceptance_data)
        
#         return {
#             "message": "NDA accepted successfully",
#             "acceptance_id": str(result.inserted_id)
#         }
    
#     @staticmethod
#     def has_accepted_nda(user_id: str) -> bool:
#         """Check if user has accepted current NDA version"""
#         acceptance = nda_acceptances_collection.find_one({
#             "user_id": user_id,
#             "nda_version": settings.NDA_VERSION,
#             "is_active": True
#         })
#         return acceptance is not None
    
#     @staticmethod
#     def get_user_nda_acceptance(user_id: str) -> Optional[dict]:
#         """Get user's NDA acceptance record"""
#         acceptance = nda_acceptances_collection.find_one({
#             "user_id": user_id,
#             "nda_version": settings.NDA_VERSION,
#             "is_active": True
#         })
        
#         if acceptance:
#             acceptance["id"] = str(acceptance.pop("_id"))
        
#         return acceptance


# services/nda_service.py
from datetime import datetime
from typing import Optional
from database import nda_acceptances_collection, users_collection
from bson import ObjectId

# Hardcoded NDA version — no config/settings needed
NDA_VERSION = "1.0"

class NDAService:
    @staticmethod
    def get_nda_content() -> dict:
        """Get current NDA content"""
        return {
            "title": "Non-Disclosure Agreement",
            "version": NDA_VERSION,  # ✅ Now uses local constant
            "content": """
NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement ("Agreement") is entered into as of the date of acceptance 
between SAYeTECH ("Disclosing Party") and the undersigned ("Receiving Party").

1. CONFIDENTIAL INFORMATION
The Receiving Party acknowledges that all information, documents, data, and materials 
provided through the SAYeTECH Investor Dataroom constitute confidential and proprietary 
information.

2. OBLIGATIONS
The Receiving Party agrees to:
- Maintain strict confidentiality of all information received
- Use the information solely for evaluation purposes
- Not disclose information to any third party without written consent
- Return or destroy all confidential information upon request

3. TERM
This Agreement shall remain in effect for a period of 5 years from the date of acceptance.

4. REMEDIES
The Receiving Party acknowledges that breach of this Agreement may cause irreparable harm 
and that monetary damages may be inadequate.

By digitally signing below, you acknowledge that you have read, understood, and agree to 
be bound by the terms of this Non-Disclosure Agreement.
            """,
            "effective_date": datetime.utcnow()
        }
    
    @staticmethod
    def accept_nda(user_id: str, digital_signature: str, ip_address: str, user_agent: str) -> dict:
        """Record NDA acceptance"""
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise ValueError("User not found")
        
        # Check if user has already accepted current NDA version
        existing_acceptance = nda_acceptances_collection.find_one({
            "user_id": user_id,
            "nda_version": NDA_VERSION,  # 
            "is_active": True
        })
        
        if existing_acceptance:
            return {
                "message": "NDA already accepted",
                "acceptance_id": str(existing_acceptance["_id"])
            }
        
        # Create new acceptance record
        acceptance_data = {
            "user_id": user_id,
            "nda_version": NDA_VERSION,  # ✅
            "digital_signature": digital_signature,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "accepted_at": datetime.utcnow(),
            "is_active": True
        }
        
        result = nda_acceptances_collection.insert_one(acceptance_data)
        return {
            "message": "NDA accepted successfully",
            "acceptance_id": str(result.inserted_id)
        }
    
    @staticmethod
    def has_accepted_nda(user_id: str) -> bool:
        """Check if user has accepted current NDA version"""
        acceptance = nda_acceptances_collection.find_one({
            "user_id": user_id,
            "nda_version": NDA_VERSION,  # ✅
            "is_active": True
        })
        return acceptance is not None
    
    @staticmethod
    def get_user_nda_acceptance(user_id: str) -> Optional[dict]:
        """Get user's NDA acceptance record"""
        acceptance = nda_acceptances_collection.find_one({
            "user_id": user_id,
            "nda_version": NDA_VERSION,  # ✅
            "is_active": True
        })
        
        if acceptance:
            acceptance["id"] = str(acceptance.pop("_id"))
        return acceptance