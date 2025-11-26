# # # from pydantic import BaseModel,Field
# # # from datetime import datetime
# # # from typing import Optional

# # # class NDAAcceptance(BaseModel):
# # #     user_id: str
# # #     accepted_at: datetime = Field(default_factory=datetime.utcnow)
# # #     ip_address: Optional[str] = None
# # #     user_agent: Optional[str] = None

# # # class NDAResponse(BaseModel):
# # #     nda_id: str  
# # #     title: str
# # #     version: str
# # #     content: str
# # #     ip_address: Optional[str] = None
# # #     user_agent: Optional[str] = None
# # #     effective_date: datetime
# # #     created_at: datetime  
    
# # # class NDASignRequest(BaseModel):
# # #     investor_id: str
# # #     ip_address: Optional[str] = None
    
# # # class NDASignResponse(BaseModel):
# # #     message: str
# # #     signed_at: datetime
# # #     nda_id: str


# # # models/nda.py
# # from pydantic import BaseModel, Field
# # from typing import Optional
# # from datetime import datetime

# # class NDAAcceptance(BaseModel):
# #     user_id: str
# #     nda_version: str
# #     accepted_at: datetime = Field(default_factory=datetime.utcnow)
# #     ip_address: Optional[str] = None
# #     user_agent: Optional[str] = None
# #     signature: Optional[str] = None

# # class NDAResponse(BaseModel):
# #     id: str
# #     user_id: str
# #     nda_version: str
# #     accepted_at: datetime
# #     ip_address: Optional[str] = None
# #     user_agent: Optional[str] = None
# #     signature: Optional[str] = None
    
# #     class Config:
# #         from_attributes = True

# # class NDAContent(BaseModel):
# #     content: str
# #     version: str
# #     effective_date: datetime
# #     updated_at: datetime = Field(default_factory=datetime.utcnow)
# #     is_active: bool = True

# # class NDASignRequest(BaseModel):
# #     nda_version: str
# #     signature: str
# #     ip_address: Optional[str] = None
# #     user_agent: Optional[str] = None

# # class NDASignResponse(BaseModel):
# #     success: bool
# #     message: str
# #     nda_id: Optional[str] = None
# #     accepted_at: Optional[datetime] = None

# # models/nda.py
# from pydantic import BaseModel, Field
# from typing import Optional
# from datetime import datetime

# class NDAAcceptance(BaseModel):
#     user_id: str
#     nda_version: str
#     accepted_at: datetime = Field(default_factory=datetime.utcnow)
#     ip_address: Optional[str] = None
#     user_agent: Optional[str] = None
#     signature: Optional[str] = None

# class NDAResponse(BaseModel):
#     nda_id: str  # Changed from 'id' to 'nda_id'
#     user_id: str
#     nda_version: str
#     accepted_at: datetime
#     content: str
#     created_at: datetime  # Added this field
#     ip_address: Optional[str] = None
#     user_agent: Optional[str] = None
#     signature: Optional[str] = None
    
#     class Config:
#         from_attributes = True

# class NDAContent(BaseModel):
#     content: str
#     version: str
#     effective_date: datetime
#     updated_at: datetime = Field(default_factory=datetime.utcnow)
#     is_active: bool = True

# class NDASignRequest(BaseModel):
#     nda_version: str
#     signature: str
#     ip_address: Optional[str] = None
#     user_agent: Optional[str] = None

# class NDASignResponse(BaseModel):
#     success: bool
#     message: str
#     nda_id: Optional[str] = None
#     accepted_at: Optional[datetime] = None

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NDAAcceptance(BaseModel):
    digital_signature: str
    ip_address: str
    user_agent: str


class NDAResponse(BaseModel):
    id: str
    user_id: str
    nda_version: str
    digital_signature: str
    ip_address: str
    accepted_at: datetime
    is_active: bool


class NDAContent(BaseModel):
    version: str
    content: str
    effective_date: datetime