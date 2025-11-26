# # from fastapi import APIRouter, HTTPException, Depends, Request
# # from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# # from models.nda import NDAAcceptance, NDAResponse, NDAContent
# # from services.nda_service import NDAService
# # from services.auth_service import AuthService

# # router = APIRouter(prefix="/api/nda", tags=["NDA"])
# # security = HTTPBearer()

# # def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
# #     """Extract user ID from JWT token"""
# #     token = credentials.credentials
# #     payload = AuthService.verify_token(token)
    
# #     if not payload:
# #         raise HTTPException(status_code=401, detail="Invalid or expired token")
    
# #     return payload["sub"]

# # @router.get("/content", response_model=NDAContent)
# # def get_nda_content():
# #     """Get current NDA content"""
# #     return NDAService.get_nda_content()

# # @router.post("/accept")
# # def accept_nda(
# #     nda_acceptance: NDAAcceptance,
# #     request: Request,
# #     user_id: str = Depends(get_current_user_id)
# # ):
# #     """Accept NDA agreement"""
# #     try:
# #         result = NDAService.accept_nda(
# #             user_id=user_id,
# #             digital_signature=nda_acceptance.digital_signature,
# #             ip_address=nda_acceptance.ip_address or request.client.host,
# #             user_agent=nda_acceptance.user_agent or request.headers.get("user-agent", "")
# #         )
# #         return result
# #     except ValueError as e:
# #         raise HTTPException(status_code=400, detail=str(e))

# # @router.get("/status")
# # def check_nda_status(user_id: str = Depends(get_current_user_id)):
# #     """Check if user has accepted NDA"""
# #     has_accepted = NDAService.has_accepted_nda(user_id)
# #     acceptance = NDAService.get_user_nda_acceptance(user_id) if has_accepted else None
    
# #     return {
# #         "has_accepted": has_accepted,
# #         "acceptance": acceptance
# #     }


# from fastapi import APIRouter, HTTPException
# from datetime import datetime
# from models.nda import NDAResponse, NDASignRequest, NDASignResponse
# from database import db
# from bson import ObjectId

# router = APIRouter(prefix="/api/nda", tags=["NDA"])

# @router.get("/current", response_model=NDAResponse)
# async def get_current_nda():
#     """Get the current active NDA"""
    
#     # Check if NDA exists in database
#     nda = db["ndas"].find_one({"is_active": True})
    
#     if not nda:
#         # Create default NDA if none exists
#         nda_data = {
#             "title": "Non-Disclosure Agreement",
#             "version": "1.0",
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
#             "effective_date": datetime.utcnow(),
#             "created_at": datetime.utcnow(),
#             "is_active": True
#         }
        
#         result = db["ndas"].insert_one(nda_data)
#         nda = db["ndas"].find_one({"_id": result.inserted_id})
    
#     # Convert MongoDB document to response format
#     return NDAResponse(
#         nda_id=str(nda["_id"]),  # ADD THIS
#         title=nda["title"],
#         version=nda["version"],
#         content=nda["content"],
#         effective_date=nda["effective_date"],
#         created_at=nda["created_at"]  # ADD THIS
#     )

# @router.post("/sign", response_model=NDASignResponse)
# async def sign_nda(sign_request: NDASignRequest):
#     """Sign the NDA"""
    
#     # Get current NDA
#     nda = db["ndas"].find_one({"is_active": True})
#     if not nda:
#         raise HTTPException(status_code=404, detail="No active NDA found")
    
#     # Record signature
#     signature_data = {
#         "nda_id": str(nda["_id"]),
#         "investor_id": sign_request.investor_id,
#         "signed_at": datetime.utcnow(),
#         "ip_address": sign_request.ip_address,
#         "nda_version": nda["version"]
#     }
    
#     db["nda_signatures"].insert_one(signature_data)
    
#     return NDASignResponse(
#         message="NDA signed successfully",
#         signed_at=signature_data["signed_at"],
#         nda_id=str(nda["_id"])
#     )

# @router.get("/signed/{investor_id}")
# async def check_nda_signed(investor_id: str):
#     """Check if investor has signed the NDA"""
    
#     signature = db["nda_signatures"].find_one({
#         "investor_id": investor_id
#     })
    
#     return {
#         "has_signed": signature is not None,
#         "signed_at": signature["signed_at"] if signature else None
#     }


from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.nda import NDAAcceptance, NDAResponse, NDAContent
from services.nda_service import NDAService
from services.auth_service import AuthService

router = APIRouter(prefix="/api/nda", tags=["NDA"])
security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extract user ID from JWT token"""
    token = credentials.credentials
    payload = AuthService.verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload["sub"]

@router.get("/content", response_model=NDAContent)
def get_nda_content():
    """Get current NDA content"""
    return NDAService.get_nda_content()

@router.post("/accept")
def accept_nda(
    nda_acceptance: NDAAcceptance,
    request: Request,
    user_id: str = Depends(get_current_user_id)
):
    """Accept NDA agreement"""
    try:
        result = NDAService.accept_nda(
            user_id=user_id,
            digital_signature=nda_acceptance.digital_signature,
            ip_address=nda_acceptance.ip_address or request.client.host,
            user_agent=nda_acceptance.user_agent or request.headers.get("user-agent", "")
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status")
def check_nda_status(user_id: str = Depends(get_current_user_id)):
    """Check if user has accepted NDA"""
    has_accepted = NDAService.has_accepted_nda(user_id)
    acceptance = NDAService.get_user_nda_acceptance(user_id) if has_accepted else None
    
    return {
        "has_accepted": has_accepted,
        "acceptance": acceptance
    }