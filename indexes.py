from pymongo import ASCENDING
from database import access_tokens_collection, users_collection, otp_codes_collection, permission_levels_collection, document_categories_collection

# Create indexes
access_tokens_collection.create_index([("token", ASCENDING)], unique=True)
users_collection.create_index([("email", ASCENDING)], unique=True)
otp_codes_collection.create_index([("email", ASCENDING)])
otp_codes_collection.create_index([("expires_at", ASCENDING)], expireAfterSeconds=0)
permission_levels_collection.create_index([("name", ASCENDING)], unique=True)
document_categories_collection.create_index([("slug", ASCENDING)], unique=True)