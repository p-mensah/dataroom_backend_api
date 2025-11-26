
from pymongo import MongoClient, ASCENDING, TEXT
from config import settings

client = MongoClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]

# Existing Collections
access_requests_collection = db["access_requests"]
access_tokens_collection = db["access_tokens"]
admin_users_collection = db["admin_users"]
audit_logs_collection = db["audit_logs"]
investors_collection = db["investors"]
documents_collection = db["documents"]
document_access_collection = db["document_access"]
qa_threads_collection = db["qa_threads"]
qa_responses_collection = db["qa_responses"]
meetings_collection = db["meetings"]
alert_configs_collection = db["alert_configs"]
alert_logs_collection = db["alert_logs"]
search_history_collection = db["search_history"]
company_metrics_collection = db["company_metrics"]
testimonials_collection = db["testimonials"]
system_settings_collection = db["system_settings"]
email_templates_collection = db["email_templates"]
otp_codes_collection = db["otp_codes"]
users_collection = db["users"]
nda_collection = db["nda"]
nda_acceptances_collection = db["nda_acceptances"]
permission_levels_collection = db["permission_levels"]
document_categories_collection = db["document_categories"]
document_access_logs_collection = db["document_access_logs"]

# NEW: OTP Collections
otp_codes_collection = db["otp_codes"]
otp_attempts_collection = db["otp_attempts"]

def create_indexes():
    # Existing indexes...
    documents_collection.create_index([("title", TEXT), ("description", TEXT), ("tags", TEXT)])
    documents_collection.create_index([("category", ASCENDING)])
    documents_collection.create_index([("uploaded_at", ASCENDING)])
    document_access_collection.create_index([("investor_id", ASCENDING), ("timestamp", ASCENDING)])
    investors_collection.create_index([("email", ASCENDING)], unique=True)
    
    # NEW: OTP indexes
    otp_codes_collection.create_index([("email", ASCENDING)])
    otp_codes_collection.create_index([("expires_at", ASCENDING)])
    otp_codes_collection.create_index([("created_at", ASCENDING)], expireAfterSeconds=600)  # Auto-delete after 10 min
    otp_attempts_collection.create_index([("email", ASCENDING)])
    
    print("✅ Indexes created successfully")