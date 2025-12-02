from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from datetime import datetime
from config import settings

client = MongoClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]


# Access & Authentication
access_requests_collection = db["access_requests"]
access_tokens_collection = db["access_tokens"]
otp_codes_collection = db["otp_codes"]
otp_attempts_collection = db["otp_attempts"]

# Users & Permissions
admin_users_collection = db["admin_users"]
investors_collection = db["investors"]
users_collection = db["users"]
permission_levels_collection = db["permission_levels"]

# Documents
documents_collection = db["documents"]
document_categories_collection = db["document_categories"]
document_access_collection = db["document_access"]
document_access_logs_collection = db["document_access_logs"]
document_versions_collection = db["document_versions"]
document_views_collection = db["document_views"]

# Q&A System
qa_threads_collection = db["qa_threads"]
qa_responses_collection = db["qa_responses"]

# NDA
nda_collection = db["nda"]
nda_acceptances_collection = db["nda_acceptances"]

# Company Information
company_metrics_collection = db["company_metrics"]
key_metrics_collection = db["key_metrics"]
milestones_collection = db["milestones"]
testimonials_collection = db["testimonials"]
awards_collection = db["awards"]
media_coverage_collection = db["media_coverage"]

# System
audit_logs_collection = db["audit_logs"]
meetings_collection = db["meetings"]
alert_configs_collection = db["alert_configs"]
alert_logs_collection = db["alert_logs"]
search_history_collection = db["search_history"]
system_settings_collection = db["system_settings"]
email_templates_collection = db["email_templates"]



def setup_indexes():
    """Create all necessary database indexes"""
    
    print("Creating database indexes...")
    
    # Documents - Full text search
    documents_collection.create_index([
        ("title", TEXT),
        ("description", TEXT),
        ("tags", TEXT)
    ], name="document_search_index")
    
    # Documents - Regular indexes
    documents_collection.create_index([("category_id", ASCENDING)])
    documents_collection.create_index([("file_type", ASCENDING)])
    documents_collection.create_index([("upload_date", DESCENDING)])
    documents_collection.create_index([("view_count", DESCENDING)])
    documents_collection.create_index([("category", ASCENDING)])
    documents_collection.create_index([("uploaded_at", ASCENDING)])
    
    # Document Versions
    document_versions_collection.create_index([
        ("document_id", ASCENDING),
        ("upload_date", DESCENDING)
    ])
    document_versions_collection.create_index([("is_current", ASCENDING)])
    
    # Document Access & Views
    document_access_collection.create_index([
        ("investor_id", ASCENDING),
        ("timestamp", ASCENDING)
    ])
    document_views_collection.create_index([
        ("document_id", ASCENDING),
        ("user_id", ASCENDING),
        ("viewed_at", DESCENDING)
    ])
    
    # Search History
    search_history_collection.create_index([
        ("user_id", ASCENDING),
        ("timestamp", DESCENDING)
    ])
    
    # Q&A Threads - Full text search
    qa_threads_collection.create_index([
        ("question_text", TEXT),
        ("answer_text", TEXT)
    ], name="qa_search_index")
    
    # Q&A Threads - Regular indexes
    qa_threads_collection.create_index([("asked_by", ASCENDING)])
    qa_threads_collection.create_index([("status", ASCENDING)])
    qa_threads_collection.create_index([("is_public", ASCENDING)])
    qa_threads_collection.create_index([("category", ASCENDING)])
    
    # Users & Authentication
    investors_collection.create_index([("email", ASCENDING)], unique=True)
    admin_users_collection.create_index([("username", ASCENDING)], unique=True, sparse=True)
    admin_users_collection.create_index([("email", ASCENDING)], unique=True)
    
    # OTP indexes
    otp_codes_collection.create_index([("email", ASCENDING)])
    otp_codes_collection.create_index([("expires_at", ASCENDING)])
    otp_codes_collection.create_index([("created_at", ASCENDING)], expireAfterSeconds=600)
    otp_attempts_collection.create_index([("email", ASCENDING)])
    
    # Company Information
    key_metrics_collection.create_index([("display_order", ASCENDING)])
    milestones_collection.create_index([("date", DESCENDING)])
    testimonials_collection.create_index([("is_featured", DESCENDING)])
    awards_collection.create_index([("date_received", DESCENDING)])
    media_coverage_collection.create_index([("publish_date", DESCENDING)])
    
    print(" All indexes created successfully")


# SEED DATA - Initial company information


def seed_company_data():
    """Seed initial company information"""
    
    print("Seeding company data...")
    
    # Key Metrics
    if key_metrics_collection.count_documents({}) == 0:
        key_metrics_collection.insert_many([
            {
                "metric_name": "Annual Revenue",
                "value": "$2.5M",
                "trend": "up",
                "display_order": 1,
                "last_updated": datetime.utcnow()
            },
            {
                "metric_name": "YoY Growth",
                "value": "145%",
                "trend": "up",
                "display_order": 2,
                "last_updated": datetime.utcnow()
            },
            {
                "metric_name": "Active Customers",
                "value": "1,250",
                "trend": "up",
                "display_order": 3,
                "last_updated": datetime.utcnow()
            },
            {
                "metric_name": "Customer Retention",
                "value": "92%",
                "trend": "stable",
                "display_order": 4,
                "last_updated": datetime.utcnow()
            }
        ])
        print(" Key metrics seeded")
    
    # Milestones
    if milestones_collection.count_documents({}) == 0:
        milestones_collection.insert_many([
            {
                "date": datetime(2020, 1, 1),
                "title": "Company Founded",
                "description": "SAYeTECH officially launched with seed funding",
                "category": "funding"
            },
            {
                "date": datetime(2021, 6, 15),
                "title": "Series A Funding",
                "description": "Raised $5M in Series A funding",
                "category": "funding"
            },
            {
                "date": datetime(2022, 3, 1),
                "title": "Product Launch",
                "description": "Launched flagship product to market",
                "category": "product"
            },
            {
                "date": datetime(2023, 9, 10),
                "title": "1000+ Customers",
                "description": "Reached milestone of 1000 active customers",
                "category": "growth"
            },
            {
                "date": datetime(2024, 2, 20),
                "title": "Strategic Partnership",
                "description": "Announced partnership with Fortune 500 company",
                "category": "partnership"
            }
        ])
        print(" Milestones seeded")
    
    # Sample Testimonials
    if testimonials_collection.count_documents({}) == 0:
        testimonials_collection.insert_many([
            {
                "customer_name": "Michael Abrahams",
                "company": "TechCorp Inc.",
                "position": "CEO",
                "testimonial_text": "SAYeTECH has transformed how we manage our operations. The ROI was evident within the first quarter.",
                "rating": 5,
                "date_added": datetime.utcnow(),
                "is_featured": True
            },
            {
                "customer_name": "Attah Adwjoa",
                "company": "Innovation Labs",
                "position": "CTO",
                "testimonial_text": "Outstanding product and exceptional support team. Highly recommended!",
                "rating": 5,
                "date_added": datetime.utcnow(),
                "is_featured": True
            }
        ])
        print(" Testimonials seeded")
    
    print(" Company data seeding completed")


# MAIN SETUP

def initialize_database():
    """Initialize database with indexes and seed data"""
    print("\n" + "="*60)
    print("DATABASE INITIALIZATION")
    print("="*60 + "\n")
    
    setup_indexes()
    seed_company_data()
    
    print("\n" + "="*60)
    print(" DATABASE SETUP COMPLETE")
    print("="*60 + "\n")


# Run setup when executed directly
if __name__ == "__main__":
    initialize_database()