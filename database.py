
from pymongo import MongoClient, ASCENDING, DESCENDING
from config import settings

client = MongoClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]

# ALL Collections (11 total)
access_requests_collection = db["access_requests"]
access_tokens_collection = db["access_tokens"]
admin_users_collection = db["admin_users"]
audit_logs_collection = db["audit_logs"]
users_collection = db["users"]
otp_codes_collection = db["otp_codes"]
nda_acceptances_collection = db["nda_acceptances"]
permission_levels_collection = db["permission_levels"]
document_categories_collection = db["document_categories"]
documents_collection = db["documents"]
document_versions_collection = db["document_versions"]
document_access_logs_collection = db["document_access_logs"]

# Create indexes
def create_indexes():
    access_tokens_collection.create_index([("token", ASCENDING)], unique=True)
    users_collection.create_index([("email", ASCENDING)], unique=True)
    otp_codes_collection.create_index([("email", ASCENDING)])
    otp_codes_collection.create_index([("expires_at", ASCENDING)], expireAfterSeconds=0)
    permission_levels_collection.create_index([("name", ASCENDING)], unique=True)
    document_categories_collection.create_index([("slug", ASCENDING)], unique=True)
    print("Indexes created")

try:
    create_indexes()
except:
    pass